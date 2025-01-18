while true; do
  ffmpeg -re \
    -headers "Referer: " \
    -i "https://buddyxiptv.com/fancode/global/primary/116279_english_hls_6566ta-no/480p.m3u8" \
    -c:v libx264 -preset superfast -b:v 3000k \
    -c:a aac -b:a 128k \
    -ar 44100 -ac 2 \
    -f flv "rtmp://vsu.okcdn.ru/input/9087506587194_7666688264762_xvdxpkp5cm" \
    -timeout 5000000 \
    -reconnect 1 \
    -reconnect_streamed 1 \
    -reconnect_delay_max 2

  echo "Stream disconnected. Reconnecting in 5 seconds..."
  sleep 5
done
