// Test para verificar si las notificaciones funcionan
// Ejecutar en la consola del navegador después de iniciar sesión

// 1. Obtener token del localStorage
const token = localStorage.getItem('token');
if (!token) {
    console.error('❌ No hay token. Inicia sesión primero.');
    throw new Error('Token no encontrado');
}

// 2. Test de notificación de completado
async function testNotificacionCompletado() {
    console.log('🧪 Test de notificación de completado...');
    
    try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/notificaciones/verificar-pasante/TU_ID', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        console.log('✅ Respuesta:', data);
        
        if (data.message && data.message.includes('diagnóstico')) {
            console.log('📊 Diagnóstico completado. Revisa la consola del backend.');
        }
        
    } catch (error) {
        console.error('❌ Error:', error);
    }
}

// 3. Test de notificación de cerca de completar
async function testNotificacionCerca() {
    console.log('🧪 Test de notificación de cerca de completar...');
    
    try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/notificaciones/verificar-cerca-completar/TU_ID', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        console.log('✅ Respuesta:', data);
        
        if (data.message && data.message.includes('cerca')) {
            console.log('📊 Verificación de cerca completada. Revisa la consola del backend.');
        }
        
    } catch (error) {
        console.error('❌ Error:', error);
    }
}

// 4. Test de configuración de correo
async function testConfiguracionCorreo() {
    console.log('🧪 Test de configuración de correo...');
    
    try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/notificaciones/test-email', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                to: 'tu_correo@ejemplo.com', // Reemplaza con tu correo
                subject: 'Test de notificación',
                body: 'Este es un test para verificar que las notificaciones funcionan.'
            })
        });
        
        const data = await response.json();
        console.log('✅ Respuesta:', data);
        
    } catch (error) {
        console.error('❌ Error:', error);
    }
}

// 5. Función principal
async function runTests() {
    console.log('🚀 Iniciando tests de notificaciones...');
    console.log('⚠️ Reemplaza TU_ID con tu ID de pasante real');
    
    // Obtener ID del usuario actual
    try {
        const userResponse = await fetch('http://127.0.0.1:8000/api/v1/usuarios/perfil', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const userData = await userResponse.json();
        console.log('👤 Usuario actual:', userData);
        
        if (userData.id) {
            console.log(`✅ ID de usuario encontrado: ${userData.id}`);
            console.log('📝 Ahora reemplaza TU_ID con este ID en los tests.');
        }
        
    } catch (error) {
        console.error('❌ Error obteniendo perfil:', error);
    }
}

// Exportar funciones para usarlas manualmente
window.testNotificaciones = {
    runTests,
    testNotificacionCompletado,
    testNotificacionCerca,
    testConfiguracionCorreo
};

console.log('📋 Funciones cargadas. Usa:');
console.log('  window.testNotificaciones.runTests()');
console.log('  window.testNotificaciones.testNotificacionCompletado()');
console.log('  window.testNotificaciones.testNotificacionCerca()');
console.log('  window.testNotificaciones.testConfiguracionCorreo()');
