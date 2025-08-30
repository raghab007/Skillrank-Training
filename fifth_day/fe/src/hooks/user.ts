import { useEffect, useState, useCallback } from "react";
import { axiosInstance } from "../api/apis";
import type { IUser } from "../pages/User";

function useFetchUsersData(url: string) {
    const [users, setUsers] = useState<IUser[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);
    const [count, setCount] = useState(0)

    const fetchData = useCallback(async () => {
        setLoading(true);
        try {
            const response = await axiosInstance.get(url);
            setUsers(response.data.users);
            setCount(response.data.count);
            setError(false);
        } catch (error) {
            setError(true);
            console.log(error);
        } finally {
            setLoading(false);
        }
    }, [url]);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    return { users, loading, error, count, refetch: fetchData };
}

export { useFetchUsersData };