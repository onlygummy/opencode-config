# Ship closes the loop after the push

`ship` stopped at the PR URL, and nothing handed the next step to the user. The
first merged PR left the local checkout on the old commit, so the next session
could not see the new agent file, and the user had no reason to suspect the
local copy. `ship` now ends every run with three handoff steps: merge on the
web, delete the merged branch there, then switch to the trunk from rule 4 and
run `git pull --ff-only origin <trunk>`. When the user reports a merge, the
agent syncs the trunk itself and stops.

Merge and branch deletion stay manual because both are denied for this agent.
The agent only reads the result and reports the new trunk SHA.
