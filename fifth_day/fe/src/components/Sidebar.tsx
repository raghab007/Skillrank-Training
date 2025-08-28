import { Link, useLocation } from "react-router-dom";

function Sidebar() {
    const location = useLocation();

    const menuItems = [
        { name: "Dashboard", path: "/dashboard" },
        { name: "Add User", path: "/add-user" },
        { name: "Users", path: "/users" },
    ];

    const isActive = (path: string) => location.pathname === path;

    return (
        <div className="h-screen w-64 bg-gray-900 text-white flex flex-col">
            {/* Header */}
            <div className="p-6 border-b border-gray-700">
                <h1 className="text-xl font-semibold">MyApp</h1>
            </div>

            {/* Navigation */}
            <nav className="flex-1 p-4">
                <ul className="space-y-2">
                    {menuItems.map((item) => (
                        <li key={item.path}>
                            <Link
                                to={item.path}
                                className={`block px-4 py-3 rounded-lg transition-colors ${isActive(item.path)
                                    ? 'bg-blue-600 text-white'
                                    : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                                    }`}
                            >
                                {item.name}
                            </Link>
                        </li>
                    ))}
                </ul>
            </nav>
        </div>
    );
}

export default Sidebar;