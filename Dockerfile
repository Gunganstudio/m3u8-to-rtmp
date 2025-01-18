FROM alpine:latest

COPY --from=mwader/static-ffmpeg:5.0 /ffmpeg /usr/local/bin/
COPY --from=mwader/static-ffmpeg:5.0 /ffprobe /usr/local/bin/

CMD set -xeu && : https://buddyxiptv.com/fancode/global/primary/116279_english_hls_6566ta-no/480p.m3u8  && : rtmp://vsu.okcdn.ru/input/9087506587194_7666688264762_xvdxpkp5cm && while :; do ffmpeg -re -stats -loglevel info -fflags +genpts -i ${STREAM_IN} -codec:v copy -vsync 0 -copyts -start_at_zero -codec:a copy -bsf:a aac_adtstoasc -f flv ${STREAM_OUT};sleep 5; echo RESTARTING...; done
