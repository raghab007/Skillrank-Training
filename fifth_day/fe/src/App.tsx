import { Route, Routes } from "react-router-dom"
import MainLayout from "./components/Layout"
import { User } from "./pages/User"
import AddUser from "./components/AddUser"

function App() {


  return (
    <>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route path="users" element={<User />} />
          <Route path="add-user" element={<AddUser />} />
        </Route>
      </Routes>

    </>
  )
}

export default App
