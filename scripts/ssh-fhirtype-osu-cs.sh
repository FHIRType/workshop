while getopts u: flag
do
    case "${flag}" in
        u) username=${OPTARG};;
        *) pass;;
    esac
done

gcloud compute ssh --zone "us-central1-a" "$username@fhirtype-test-alpha" --project "fhirtype-osu-cs"

input -r "Press [ENTER] to exit..."