#!/bin/bash

case "$1" in
    EF29)
        cd /root/build_EF29
        ./tools/target_dec_dfa_fuzzer /dataset/EF29/clusterfuzz-testcase-minimized-ffmpeg_AV_CODEC_ID_DFA_fuzzer-6062963045695488
        ;;
    EF30)
        cd /root/build_EF30
        ./tools/target_dec_cavs_fuzzer /dataset/EF30/clusterfuzz-testcase-minimized-ffmpeg_AV_CODEC_ID_CAVS_fuzzer-5000441286885376
        ;;
    *)
        echo "No such bug: $1"
        ;;
esac
