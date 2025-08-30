import { useEffect, useState } from "react";
import { axiosInstance } from "../api/apis";
import type { IUser } from "../pages/User";

function useFetchUsersData(url: string) {
    const [users, setUsers] = useState<IUser[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);
    const [count, setCount] = useState(0)

    useEffect(() => {
        axiosInstance
            .get(url)
            .then((response) => {
                setUsers(response.data.users);
                setCount(response.data.count)
                setLoading(false);
            })
            .catch((error) => {
                setError(true);
                setLoading(false);
                console.log(error)
            });
    }, [url]);

    return { users, loading, error, count };


}

export { useFetchUsersData };