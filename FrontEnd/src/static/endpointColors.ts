// Define a mapping between endpoints and colors
const endpointColors: Record<string, string> = {
    'Kaiser': '#ADD8E6', //LightBlue
    'Humana': '#E6E6FA', //Lavender
    'Cigna': '#FFE4E1', //MistyRose
    'PacificSource': '#8FBC8F', //DarkSeaGreen
    'Centene': '#D3D3D3' //DarkSlateBlue
    //other endpoints
};

// Define conditional row styles function using the endpointColors mapping
export const conditionalRowStyles = [
    {
        when: (row: { Endpoint: string }) => endpointColors.hasOwnProperty(row.Endpoint),
        style: (row: { Endpoint: string }) => ({
            backgroundColor: endpointColors[row.Endpoint],
        }),
    },
];