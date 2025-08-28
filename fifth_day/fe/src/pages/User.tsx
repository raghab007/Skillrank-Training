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
    const [isUpdating, setIsUpdating] = useState(false);
    const [updateUser, setUpdateUser] = useState<IUser>()
    const [currentPage, setCurrentPage] = useState(1)
    const pageSize = 5;
    const { users, error, count, loading } = useFetchUsersData(`/api/users/${currentPage}/${pageSize}`);

    const { users: nextUsers } = useFetchUsersData(`/api/users/${currentPage + 1}/${pageSize}`)
    const { users: previousUsers } = useFetchUsersData(`/api/users/${currentPage - 1}/${pageSize}`)
    const totalPages = Math.ceil(count / pageSize)

    if (loading) return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
            <div className="text-center">
                <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mb-4"></div>
                <p className="text-gray-600">Loading users...</p>
            </div>
        </div>
    );

    if (error) return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
            <div className="text-center bg-white p-6 rounded-lg shadow border border-gray-200 max-w-md">
                <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg className="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                    </svg>
                </div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">Something went wrong</h3>
                <p className="text-gray-500">Unable to load users. Please try again later.</p>
            </div>
        </div>
    );

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

    async function nextPage() {
        if (!nextUsers || nextUsers.length == 0) {
            alert("No more users found")
            return
        }
        setCurrentPage(current => current + 1)
    }

    async function previousPage() {
        if (!previousUsers || previousUsers.length == 0) {
            alert("No more users found")
            return
        }
        setCurrentPage(current => current - 1)
    }

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Header Section */}
                <div className="mb-8">
                    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
                        <div className="mb-4 sm:mb-0">
                            <h1 className="text-2xl font-bold text-gray-900">
                                User Management
                            </h1>
                            <p className="text-gray-600 mt-1">
                                Manage your users
                            </p>
                        </div>
                        <div className="bg-white px-4 py-2 rounded-lg border border-gray-200 shadow-sm">
                            <span className="text-gray-600">Total Users: </span>
                            <span className="font-semibold text-blue-600">{count}</span>
                        </div>
                    </div>
                </div>

                {/* Update Form Modal */}
                {isUpdating && (
                    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
                        <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4 relative shadow-lg">
                            <button
                                onClick={() => setIsUpdating(false)}
                                className="absolute top-4 right-4 text-gray-400 hover:text-gray-600"
                            >
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                                </svg>
                            </button>

                            <div className="mb-6">
                                <h3 className="text-xl font-semibold text-gray-900 mb-1">Update User</h3>
                                <p className="text-gray-600 text-sm">Update user information</p>
                            </div>

                            {updateUser && <UpdateUserForm user={updateUser} />}
                        </div>
                    </div>
                )}

                {/* Users Table */}
                <div className="bg-white rounded-lg shadow border border-gray-200 overflow-hidden">
                    {/* Table Header */}
                    <div className="bg-gray-50 px-6 py-4 border-b border-gray-200">
                        <h2 className="text-lg font-medium text-gray-900">
                            User Directory
                        </h2>
                    </div>

                    {users && users.length > 0 ? (
                        <div className="overflow-x-auto">
                            <table className="w-full">
                                <thead className="bg-gray-50">
                                    <tr>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            User
                                        </th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Contact
                                        </th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Age
                                        </th>
                                        <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Actions
                                        </th>
                                    </tr>
                                </thead>
                                <tbody className="bg-white divide-y divide-gray-200">
                                    {users?.map((user) => (
                                        <tr key={user._id} className="hover:bg-gray-50">
                                            <td className="px-6 py-4">
                                                <div className="flex items-center">
                                                    <div className="flex-shrink-0 h-10 w-10">
                                                        <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                                                            <span className="text-blue-800 font-medium">
                                                                {user.name.charAt(0).toUpperCase()}
                                                            </span>
                                                        </div>
                                                    </div>
                                                    <div className="ml-4">
                                                        <div className="text-sm font-medium text-gray-900">{user.name}</div>
                                                        <div className="text-sm text-gray-500">{user.address}</div>
                                                    </div>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4">
                                                <div className="text-sm text-gray-900">{user.email}</div>
                                                <div className="text-sm text-gray-500">{user.phone}</div>
                                            </td>
                                            <td className="px-6 py-4">
                                                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                                    {user.age} years
                                                </span>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                                <div className="flex justify-end space-x-3">
                                                    <button
                                                        onClick={() => {
                                                            setIsUpdating(true)
                                                            setUpdateUser(user)
                                                        }}
                                                        className="text-blue-600 hover:text-blue-900"
                                                    >
                                                        Edit
                                                    </button>
                                                    <button
                                                        onClick={() => handleDeleteUser(user._id)}
                                                        className="text-red-600 hover:text-red-900"
                                                    >
                                                        Delete
                                                    </button>
                                                </div>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    ) : (
                        <div className="text-center py-12">
                            <div className="mx-auto h-16 w-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                                <svg className="h-8 w-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5 0a4 4 0 11-8-4 4 4 0 018 4z" />
                                </svg>
                            </div>
                            <h3 className="text-lg font-medium text-gray-900 mb-1">No users found</h3>
                            <p className="text-gray-500">Get started by adding your first user.</p>
                        </div>
                    )}
                </div>

                {/* Pagination */}
                {users && users.length > 0 && (
                    <div className="mt-6">
                        <div className="bg-white rounded-lg shadow border border-gray-200 px-4 py-3 flex items-center justify-between">
                            <div className="flex-1 flex justify-between items-center sm:hidden">
                                <button
                                    onClick={previousPage}
                                    disabled={currentPage === 1}
                                    className={`relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md ${currentPage === 1 ? 'bg-gray-100 text-gray-400' : 'bg-white text-gray-700 hover:bg-gray-50'}`}
                                >
                                    Previous
                                </button>
                                <div className="text-sm text-gray-700">
                                    Page <span className="font-medium">{currentPage}</span> of <span className="font-medium">{totalPages}</span>
                                </div>
                                <button
                                    onClick={nextPage}
                                    disabled={currentPage >= totalPages}
                                    className={`relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md ${currentPage >= totalPages ? 'bg-gray-100 text-gray-400' : 'bg-white text-gray-700 hover:bg-gray-50'}`}
                                >
                                    Next
                                </button>
                            </div>
                            <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
                                <div>
                                    <p className="text-sm text-gray-700">
                                        Showing <span className="font-medium">{(currentPage - 1) * pageSize + 1}</span> to <span className="font-medium">{Math.min(currentPage * pageSize, count)}</span> of{' '}
                                        <span className="font-medium">{count}</span> results
                                    </p>
                                </div>
                                <div>
                                    <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                                        <button
                                            onClick={previousPage}
                                            disabled={currentPage === 1}
                                            className={`relative inline-flex items-center px-3 py-2 rounded-l-md border border-gray-300 text-sm font-medium ${currentPage === 1 ? 'bg-gray-100 text-gray-400' : 'bg-white text-gray-500 hover:bg-gray-50'}`}
                                        >
                                            Previous
                                        </button>
                                        <span className="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700">
                                            Page {currentPage} of {totalPages}
                                        </span>
                                        <button
                                            onClick={nextPage}
                                            disabled={currentPage >= totalPages}
                                            className={`relative inline-flex items-center px-3 py-2 rounded-r-md border border-gray-300 text-sm font-medium ${currentPage >= totalPages ? 'bg-gray-100 text-gray-400' : 'bg-white text-gray-500 hover:bg-gray-50'}`}
                                        >
                                            Next
                                        </button>
                                    </nav>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
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
        <form onSubmit={handleUpdateUser} className="space-y-4">
            <InputWithLabel
                type="text"
                name="name"
                label="Full Name"
                id="name"
                value={formData.name}
                onChange={handleInputChange}
            />
            <InputWithLabel
                type="email"
                name="email"
                label="Email Address"
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
                label="Phone Number"
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
                className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors font-medium"
            >
                Update User
            </button>
        </form>
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
        <div className="space-y-1">
            <label
                htmlFor={id}
                className="block text-sm font-medium text-gray-700"
            >
                {label}
            </label>
            <input
                type={type}
                id={id}
                name={name}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                required
                value={value}
                onChange={onChange}
                placeholder={`Enter ${label.toLowerCase()}`}
            />
        </div>
    );
}

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

export { User };