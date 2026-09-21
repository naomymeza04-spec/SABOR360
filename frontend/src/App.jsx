import { Routes, Route, Link } from 'react-router-dom'

function Home() {
  return (
    <div>
      <h1>Sabor 360</h1>
      <p>Sistema de gestión y control para restaurante mediante código QR.</p>
      <Link to="/login">Ingreso administrador</Link>
    </div>
  )
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<div><h1>Login</h1></div>} />
    </Routes>
  )
}