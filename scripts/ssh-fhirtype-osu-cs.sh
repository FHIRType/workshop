while getopts u:s: flag
do
    case "${flag}" in
        u) username=${OPTARG};;
        s) server=${OPTARG};;
        *) pass;;
    esac
done

gcloud compute ssh --zone "us-central1-a" "$username@$server" --project "fhirtype-osu-cs"

input -r "Press [ENTER] to exit..."