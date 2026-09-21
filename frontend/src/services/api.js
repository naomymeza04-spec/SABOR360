const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api'

export async function peticionGet(ruta) {
  const respuesta = await fetch(`${API_URL}${ruta}`)
  if (!respuesta.ok) throw new Error(`Error ${respuesta.status}`)
  return respuesta.json()
}

export async function peticionPost(ruta, datos) {
  const respuesta = await fetch(`${API_URL}${ruta}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(datos),
  })
  if (!respuesta.ok) throw new Error(`Error ${respuesta.status}`)
  return respuesta.json()
}