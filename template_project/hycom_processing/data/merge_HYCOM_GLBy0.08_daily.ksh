#!/usr/bin/ksh 

year=${YEAR}

echo "Merging for year $year."

if (( (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0) )); then
    nday=366
else
    nday=365
fi
#nday=230

#set -A days {258..258}
set -A days {1..$nday}

for day in ${days[@]} ; do
    day=$(printf "%03d" $day)

    # check if at least the first variable file exists
    if [[ -f HYCOM_GLBy0.08_ssh_${year}_${day}.nc ]]; then
        ncks --no-alphabetize -O HYCOM_GLBy0.08_ssh_${year}_${day}.nc HYCOM_GLBy0.08_merged_${year}_${day}.nc
        ncks --no-alphabetize -A HYCOM_GLBy0.08_temp_${year}_${day}.nc HYCOM_GLBy0.08_merged_${year}_${day}.nc
        ncks --no-alphabetize -A HYCOM_GLBy0.08_salt_${year}_${day}.nc HYCOM_GLBy0.08_merged_${year}_${day}.nc
        ncks --no-alphabetize -A HYCOM_GLBy0.08_u_${year}_${day}.nc HYCOM_GLBy0.08_merged_${year}_${day}.nc
        ncks --no-alphabetize -A HYCOM_GLBy0.08_v_${year}_${day}.nc HYCOM_GLBy0.08_merged_${year}_${day}.nc
        echo "Merged files for day $day"

        # optionally move original files to a backup directory
        mv -f HYCOM_GLBy0.08_ssh_${year}_${day}.nc \
        HYCOM_GLBy0.08_temp_${year}_${day}.nc \
        HYCOM_GLBy0.08_salt_${year}_${day}.nc \
        HYCOM_GLBy0.08_u_${year}_${day}.nc \
        HYCOM_GLBy0.08_v_${year}_${day}.nc \
        raw/
    else
        echo "No data for day $day, skipping merge"
    fi
done

echo "-----------------------------------"
echo "Merging completed for year $year."
