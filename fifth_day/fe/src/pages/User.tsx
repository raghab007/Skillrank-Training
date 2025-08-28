import React, { useEffect, useState } from "react";
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
    const [isUpdating, setIsUpdating] = useState(false);
    const [updateUser, setUpdateUser] = useState<IUser>()
    if (loading) return <div className="p-6">Loading...</div>;
    if (error) return <div className="p-6 text-red-600">Something went wrong</div>;

    async function handleDeleteUser(id: string) {
        try {
            const response = await axiosInstance.delete(`/api/users/${id}`)
            console.log(response.data.message)
            alert("User deleted successfully")
            window.location.reload();
        } catch (error) {
            console.log(error)
            alert("Error while deleting user")
        }
    }



    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-6">Users</h1>

            {/* Update Form Modal */}
            {isUpdating && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4 relative">
                        <button
                            onClick={() => setIsUpdating(false)}
                            className="absolute top-4 right-4 text-gray-500 hover:text-gray-800 text-xl font-bold"
                        >
                            ×
                        </button>

                        {updateUser && <UpdateUserForm user={updateUser} />}
                    </div>
                </div>
            )}

            {/* Users Table */}
            <div className="bg-white rounded-lg border overflow-hidden">
                <table className="w-full">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">Name</th>
                            <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">Email</th>
                            <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">Phone</th>
                            <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">Age</th>
                            <th className="px-4 py-3 text-center text-sm font-medium text-gray-600">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {users?.map((user) => (
                            <tr key={user._id} className="border-t hover:bg-gray-50">
                                <td className="px-4 py-3 text-sm">{user.name}</td>
                                <td className="px-4 py-3 text-sm">{user.email}</td>
                                <td className="px-4 py-3 text-sm">{user.phone}</td>
                                <td className="px-4 py-3 text-sm">{user.age}</td>
                                <td className="px-4 py-3 text-center">
                                    <button
                                        onClick={() => {
                                            setIsUpdating(true)
                                            setUpdateUser(user)
                                        }
                                        }
                                        className="text-blue-600 hover:text-blue-800 text-sm mr-3"
                                    >
                                        Edit
                                    </button>
                                    <button
                                        onClick={() => handleDeleteUser(user._id)}
                                        className="text-red-600 hover:text-red-800 text-sm"
                                    >
                                        Delete
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            <div className="flex justify-center"> <Pagination /></div>
        </div >
    );
}





interface IUser {
    _id: string;
    name: string;
    email: string;
    address: string;
    phone: string;
    age: number;
}

interface UpdateFormData {
    name: string;
    email: string;
    address: string;
    phone: string;
    age: string;
}

function UpdateUserForm({ user }: { user: IUser }) {
    const [formData, setFormData] = useState<UpdateFormData>({
        name: user.name,
        email: user.email,
        address: user.address,
        phone: user.phone,
        age: user.age.toString()
    });

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    async function handleUpdateUser(event: React.FormEvent<HTMLFormElement>) {
        try {
            event.preventDefault();

            // Convert age back to number for API
            const updateData = {
                ...formData,
                age: parseInt(formData.age)
            };

            const response = await axiosInstance.put(`/api/users/${user._id}`, updateData, {
                headers: {
                    "Content-Type": "application/json"
                }
            });

            alert("User updated successfully!");
            window.location.reload();
        } catch (error) {
            console.log(error);
            alert("Error while updating user");
        }
    }

    return (
        <>
            <form onSubmit={handleUpdateUser} className="space-y-4">
                <InputWithLabel
                    type="text"
                    name="name"
                    label="Name"
                    id="name"
                    value={formData.name}
                    onChange={handleInputChange}
                />
                <InputWithLabel
                    type="email"
                    name="email"
                    label="Email"
                    id="email"
                    value={formData.email}
                    onChange={handleInputChange}
                />
                <InputWithLabel
                    type="text"
                    name="address"
                    label="Address"
                    id="address"
                    value={formData.address}
                    onChange={handleInputChange}
                />
                <InputWithLabel
                    type="tel"
                    name="phone"
                    label="Phone"
                    id="phone"
                    value={formData.phone}
                    onChange={handleInputChange}
                />
                <InputWithLabel
                    type="number"
                    name="age"
                    label="Age"
                    id="age"
                    value={formData.age}
                    onChange={handleInputChange}
                />

                <button
                    type="submit"
                    className="w-full bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors font-medium mt-6"
                >
                    Update User
                </button>
            </form>
        </>
    );
}

interface InputWithLabelProps {
    type: string;
    name: string;
    label: string;
    id: string;
    value: string;
    onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

function InputWithLabel({ type, name, label, id, value, onChange }: InputWithLabelProps) {
    return (
        <div className="mb-4">
            <label
                htmlFor={id}
                className="block text-sm font-medium text-gray-700 mb-2"
            >
                {label}
            </label>
            <input
                type={type}
                id={id}
                name={name}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                required
                value={value}
                onChange={onChange}
            />
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
                setUsers(response.data);
                setLoading(false);
            })
            .catch(() => {
                setError(true);
                setLoading(false);
            });
    }, [url]);

    return { users, loading, error };
}



function Pagination() {
    return (
        <>
            <div className="flex space-x-5 mt-2">
                <button className="border-2  p-3  rounded-xl">Next</button>
                <button className="border-2  p-3  rounded-xl">Previous</button>
            </div>
        </>
    )
}


export { User };