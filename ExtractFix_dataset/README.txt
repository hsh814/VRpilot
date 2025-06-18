This is a reconstruction of the ExtractFix dataset from:

https://extractfix.github.io/

(Paper: https://www.comp.nus.edu.sg/~abhik/pdf/TOSEMextractfix21.pdf )

The dataset consists of 30 vulnerabilities from 7 different projects. Since
all the projects are tracked in git, I have used git branches to track the
vulnerable version (the parent commit of the commit that fixes the vuln).

Files:

bugs.txt: a list of metadata for each bug. Format:
    num repo_dir bugid patch_url
notes.txt: notes on where this dataset differs slightly from what is present
    on their web site (there was one incorrect patch URL and one ambiguous
    case where a patch was not in the main git history)
repos/*: one directory for each project's git repository (corresponding to
    repo_dir in bugs.txt). Each repo has branches named EF{num} where num is
    the bug number from bugs.txt.
patches/ExtractFix_Patch_{num}.patch:
    the patch that fixes bug numbered num. These should apply cleanly to the
    corresponding EF{num} branch.
index.html:
    saved copy of the extractfix.github.io from Nov 13, 2021
testcases/EF*.txt:
    Instructions for reproducing each bug
testcases/EF*/{asan,ubsan}*.txt:
    ASAN/UBSAN reports for each reproduced test case
README.<project>.txt:
    A readme with instructions for building each project and running its
    test suite
docker/<project>/Dockerfile:
    Dockerfile that sets up the build environment (e.g., dependencies) for
    each project
reproduced.tsv:
    Tab-separated file indicating which bugs could be reproduced
scripts/patch_asan.py:
    Script to see how well ASAN/UBSAN localize each patch, compared to the
    developer-provided fix.
scripts/patch_overlap_codeql.py:
    Script to check if any issues reported by CodeQL match the
    developer-provided fix.
