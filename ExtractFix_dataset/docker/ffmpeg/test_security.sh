#!/bin/bash

/scripts/test_build.sh $1
cd /root/build

case "$1" in
    cve_2017_9992)
        ./tools/target_dec_dfa_fuzzer /dataset/cve_2017_9992/clusterfuzz-testcase-minimized-ffmpeg_AV_CODEC_ID_DFA_fuzzer-6062963045695488
        ;;
    bugzilla_1404)
        ./tools/target_dec_cavs_fuzzer /dataset/bugzilla_1404/clusterfuzz-testcase-minimized-ffmpeg_AV_CODEC_ID_CAVS_fuzzer-5000441286885376
        ;;
    *)
        echo "No such bug: $1"
        ;;
esac
