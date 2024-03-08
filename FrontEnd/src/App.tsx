import { FormEvent, useState} from 'react'
import { useQuery } from '@tanstack/react-query'
import { useSearchParams } from 'react-router-dom'

import LoadingIndicator from "./components/LoadingIndicator.tsx";
import './App.css'


export default function App() {
    const [searchParams, setSearchParams] = useSearchParams()
    const query = searchParams.get("q")
    const [fullName, setFullName] = useState("");

    const { isLoading, error, data } = useQuery({
        queryKey: ["searchPractitioner", query],
        queryFn: async () => {
            // const lengthQuery = inputQuery.length > 0 ? `&length=${inputQuery.length}` : '';
            // const response = await fetch(`http://127.0.0.1:5000/api/getdata?first_name=${searchParams.get('first_name')}&last_name=${searchParams.get('last_name')}`);
            const response = await fetch('http://127.0.0.1:5000/api/getdata?first_name=Matthew&last_name=Sleasman&npi=1326071937');
            if (!response.ok) {
                throw new Error('Failed to fetch data');
            }

            return response.json();
        }
    });

    const handleSubmit = (e: FormEvent) => {
        e.preventDefault();
        setSearchParams({ q: fullName});
    };

    return (
        <div className="container">
            {/*<form onSubmit={e => {*/}
            {/*    e.preventDefault()*/}
            {/*    setSearchParams({ q: inputQuery })*/}
            {/*}}>*/}
            <form onSubmit={handleSubmit}>
                <input className="input" value={fullName} onChange={e => setFullName(e.target.value)} placeholder="Enter Full Name" />
                <button className="button" type="submit">Search</button>
            </form>

            {isLoading ? (
                <LoadingIndicator/>
            ) : error ? (
                <div className="error">Error: {error.message}</div>
            ) : data ? (
                <div className="pract">
                    <h2>Name:</h2>
                    <p>{data.name}</p>
                </div>
            ) : null}
        </div>
    );
}
