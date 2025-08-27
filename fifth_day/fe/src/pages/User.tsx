import { useEffect, useState } from "react";
import { axiosInstance } from "../api/apis";

interface IUser {
    name: string;
    _id: string;
    email: string;
    age: number;
    address: string;
    phone: string;
}

function User() {
    const { users, error, loading } = useFetchUsersData("/api/users/1/10");

    if (error) {
        return <h1>Something went wrong</h1>;
    }

    if (loading) {
        return <h1>Loading...</h1>;
    }
    return (
        <div>
            <table>
                <tr className="">
                    <th>Name</th>
                    <th>Email</th>
                    <th>Address</th>
                    <th>Phone</th>
                    <th>Age</th>
                    <th>Actions</th>
                </tr>

                {users?.map((user) => (
                    <tr>
                        <td>{user.name}</td>
                        <td>{user.email}</td>
                        <td>{user.address}</td>
                        <td>{user.phone}</td>
                        <td>{user.age}</td>
                        <td>Delete</td>
                        <td>Update</td>
                    </tr>
                ))}
            </table>
        </div>
    );
}


function useFetchUsersData(url: string) {
    const [users, setUsers] = useState<IUser[]>();
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);
    useEffect(() => {
        axiosInstance
            .get(url)
            .then((response) => {
                console.log(response.data);
                setUsers(response.data);
                setLoading(false);
            })
            .catch((error) => {
                console.log(error);
                setError(true);
            });
    }, []);

    return { users, loading, error };
}

export { User };
