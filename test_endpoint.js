// Test para verificar si el backend funciona
fetch('http://127.0.0.1:8000/api/v1/asistencias/publico/entrada', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    username: 'postgres' // reemplaza con un username real
  })
})
.then(response => response.json())
.then(data => console.log('Respuesta:', data))
.catch(error => console.error('Error:', error))
