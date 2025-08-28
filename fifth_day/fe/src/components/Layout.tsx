import { Outlet } from "react-router-dom";
import Sidebar from "./Sidebar";

function MainLayout() {
    return (
        <div className="flex min-h-screen">
            {/* Sidebar */}
            <Sidebar />

            {/* Main content */}
            <div className="flex-1 bg-gray-50">
                <Outlet />
            </div>
        </div>
    );
}

export default MainLayout;