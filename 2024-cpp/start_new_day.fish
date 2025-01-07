#!/usr/bin/env fish

set day $argv[1]
set padded_day (string pad --width=2 --char="0" $day)
set source_dir "2024-00"
set target_dir "2024-$padded_day"

if ! string match -qr '^\d\d?$' $day
    echo "🤷 usage: ./start_new_day.sh DAY_NUMBER"
    exit 1
end

if ! test -d $source_dir
    echo "🤷 Source directory 2024-00 not found"
    exit 1
end

if test -d $target_dir
    echo "🙅 Target directory $target_dir already exists"
    exit 1
end

cp -r $source_dir $target_dir
echo "✅ Copied $source_dir to $target_dir"
cd $target_dir
