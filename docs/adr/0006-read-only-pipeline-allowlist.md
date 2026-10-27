# A read-only pipeline needs one allow per cmdlet

The plan agent could list a directory but not format the listing.
`Get-ChildItem -Force` was allowed and returned rows, while
`Get-ChildItem -Force | Select-Object Mode,Name | Format-Table -AutoSize`
returned `permission.rejected`. The scanner emits one shell resource per command
in a compound line, and the permission check applies to each resource. The first
segment matched `Get-ChildItem *`. The two later segments matched nothing, so the
blanket `shell *` deny in `agents/plan.md` won.

Two consequences follow. An allow for the whole pipeline as a single string can
never match, because the line is never checked as one resource. And every stage
in a pipeline needs its own rule, so a pipeline is only as permitted as its
least-permitted command.

`plan` and `review` now allow a closed set of read-only PowerShell cmdlets:
`Select-Object`, `Format-Table`, `Format-List`, `Sort-Object`, `Measure-Object`,
`Get-Member`, and `ConvertTo-Json`. `review` already allowed `Select-Object` for
head and tail, so it gains the other six only.

`ForEach-Object` and `Where-Object` are excluded on purpose even though they
would make pipelines more useful. Their main argument is a script block, so
allowing them grants arbitrary code execution, and that script block can call
the write commands the permission layer otherwise blocks. `Tee-Object`,
`Out-File`, and `Export-*` are excluded because they write files from inside a
pipeline that looks read-only.

Three alternatives were rejected. Allowing the whole command line fails for the
reason above. Setting `ask` on the cmdlets still needs an allow to beat the
blanket deny, and it would prompt on nearly every listing. Putting the rules in
the global `permissions` list fails because both agents deny shell after the
global rules load, so the global entry never applies to them.

Open question: `Select-Object`, `Sort-Object`, and `Measure-Object` accept
calculated properties such as `@{Name='t';Expression={Get-Date}}`. Whether the
scanner descends into those braces is unverified. If it does not, the same
escape already exists for the long-standing `Write-Output *` allow. Probe with
a script block that calls a command which has no allow rule, and record the
outcome here once the answer is known.
