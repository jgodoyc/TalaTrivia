import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Home from "./components/Home";
import Login from "./components/Login";
import PrivateRoute from "./components/PrivateRoute";
import Welcome from "./components/Welcome";
import AdminView from "./components/AdminView";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/home/*"
          element={
            <PrivateRoute>
              <Home />
            </PrivateRoute>
          }
        />
        <Route
          path="/admin"
          element={
            <PrivateRoute>
              <AdminView />
            </PrivateRoute>
          }
        />
        <Route path="/" element={<Welcome />} />
        <Route path="*" element={<Navigate to="/" />} /> {}
      </Routes>
    </Router>
  );
}

export default App;
