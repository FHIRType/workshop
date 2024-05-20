// Define a mapping between endpoints and colors
const endpointColors: Record<string, string> = {
    'Kaiser': '#ADD8E6',
    'Humana': '#E6E6FA',
    'Cigna': '#FFE4E1',
    'PacificSource': '#8FBC8F',
    'Centene': '#D3D3D3',
    'Consensus': "#64a1ec"
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