import React, { useEffect, useState } from 'react';

interface DataItem {
    PlayerName: string;
    CharacterName: string;
    Class: string;
    "DPS Skill"?: number;
    "Healer Skill"?: number;
    Dungeon: string;
    "Key Level": number;
    Range: string;
    Role: string[];
    "Skill Level": number;
    is_active: number;
}

const Table: React.FC = () => {
    const [data, setData] = useState<DataItem[]>([]);
    const [columns, setColoumns] = useState<string[]>([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch("http://localhost:5000/groups/api/current-players");
                const jsonData: DataItem[] = await response.json();

                setData(jsonData);

                if (jsonData.length > 0) {
                    setColoumns(Object.keys(jsonData[0]));
                }
            } catch (error) {
                console.error("Error fetching data:", error)
            }
        };

        fetchData();
    }, []);

    return (
        <div className='container mt-5 table-responsive-lg'>
        <table className='table table-striped table-hover '>
        <thead className='table-dark'>
            <tr>
                {columns.map((col) => (
                    <th key={col}>{col}</th>
                ))}
            </tr>
        </thead>
        <tbody>
            {data.map((row: DataItem, rowIndex: number) => (
                <tr key={rowIndex}>
                    {columns.map((col) => (
                        <td key={`${rowIndex}-${col}`}>{row[col as keyof DataItem]}</td>
                    ))}
                </tr>
            ))}
        </tbody>
    </table>
    </div>
    );
};

export default Table