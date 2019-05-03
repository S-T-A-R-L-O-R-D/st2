# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

from st2common.constants import action as action_constants
from st2common import log as logging
from st2common.persistence import action as action_access
from st2common.policies.concurrency import BaseConcurrencyApplicator
from st2common.services import action as action_service


__all__ = [
    'ConcurrencyApplicator'
]

LOG = logging.getLogger(__name__)


class ConcurrencyApplicator(BaseConcurrencyApplicator):

    def __init__(self, policy_ref, policy_type, threshold=0, action='delay'):
        super(ConcurrencyApplicator, self).__init__(policy_ref=policy_ref, policy_type=policy_type,
                                                    threshold=threshold,
                                                    action=action)

    def _get_lock_uid(self, target):
        values = {'policy_type': self._policy_type, 'action': target.action}
        return self._get_lock_name(values=values)

    def _apply_before(self, target):
        # Get the count of scheduled instances of the action.
        scheduled = action_access.LiveAction.count(
            action=target.action, status=action_constants.LIVEACTION_STATUS_SCHEDULED)

        # Get the count of running instances of the action.
        running = action_access.LiveAction.count(
            action=target.action, status=action_constants.LIVEACTION_STATUS_RUNNING)

        count = scheduled + running

        # Mark the execution as scheduled if threshold is not reached or delayed otherwise.
        if count < self.threshold:
            LOG.debug('There are %s instances of %s in scheduled or running status. '
                      'Threshold of %s is not reached. Action execution will be scheduled.',
                      count, target.action, self._policy_ref)
            status = action_constants.LIVEACTION_STATUS_REQUESTED
        else:
            action = 'delayed' if self.policy_action == 'delay' else 'canceled'
            LOG.debug('There are %s instances of %s in scheduled or running status. '
                      'Threshold of %s is reached. Action execution will be %s.',
                      count, target.action, self._policy_ref, action)
            status = self._get_status_for_policy_action(action=self.policy_action)

        # Update the status in the database. Publish status for cancellation so the
        # appropriate runner can cancel the execution. Other statuses are not published
        # because they will be picked up by the worker(s) to be processed again,
        # leading to duplicate action executions.
        publish = (status == action_constants.LIVEACTION_STATUS_CANCELING)
        target = action_service.update_status(target, status, publish=publish)

        return target

    def apply_before(self, target):
        target = super(ConcurrencyApplicator, self).apply_before(target=target)

        valid_states = [
            action_constants.LIVEACTION_STATUS_REQUESTED,
            action_constants.LIVEACTION_STATUS_DELAYED,
            action_constants.LIVEACTION_STATUS_POLICY_DELAYED,
        ]

        # Exit if target not in valid state.
        if target.status not in valid_states:
            LOG.debug('The live action is not in a valid state therefore the policy '
                      '"%s" cannot be applied. %s', self._policy_ref, target)
            return target

        target = self._apply_before(target)

        return target
