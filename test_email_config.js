// Test para verificar configuración de correo
// Ejecutar en la consola del navegador después de iniciar sesión como admin/encargado

async function testEmailConfig() {
    console.log('📧 Verificando configuración de correo...');
    
    // 1. Obtener token
    const token = localStorage.getItem('token');
    if (!token) {
        console.error('❌ No hay token. Inicia sesión como admin o encargado.');
        return;
    }
    
    // 2. Test de configuración de correo
    try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/notificaciones/test-email', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                to: 'tu_correo_de_prueba@gmail.com', // Reemplaza con tu correo
                subject: '🧪 Test de Sistema de Notificaciones',
                body: 'Este es un correo de prueba para verificar que el sistema de notificaciones funciona correctamente.\n\nSi recibes este correo, el sistema está configurado correctamente.'
            })
        });
        
        const data = await response.json();
        console.log('📊 Respuesta del test:', data);
        
        if (data.success) {
            console.log('✅ Correo enviado exitosamente. Revisa tu bandeja de entrada.');
        } else {
            console.error('❌ Error al enviar correo:', data.message);
            console.log('🔍 Estado de configuración:', data.config_status);
        }
        
    } catch (error) {
        console.error('❌ Error en la petición:', error);
    }
}

// 3. Forzar notificación de completado
async function testNotificationCompletion() {
    console.log('🎯 Forzando notificación de completado...');
    
    const token = localStorage.getItem('token');
    if (!token) {
        console.error('❌ No hay token.');
        return;
    }
    
    // Obtener información del usuario actual
    try {
        const perfilResponse = await fetch('http://127.0.0.1:8000/api/v1/usuarios/perfil', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const perfil = await perfilResponse.json();
        console.log('👤 Perfil:', perfil);
        
        // Forzar verificación de notificación
        const notifResponse = await fetch(`http://127.0.0.1:8000/api/v1/notificaciones/verificar-pasante/${perfil.id}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        const notifData = await notifResponse.json();
        console.log('📧 Resultado de notificación:', notifData);
        
        if (notifData.notificado_completado || notifData.notificado_cerca) {
            console.log('✅ Notificación procesada. Revisa la consola del backend y tu correo.');
        } else {
            console.log('ℹ️ No se enviaron notificaciones. Posibles razones:');
            console.log('  - No cumple las condiciones (240h o 220-239h)');
            console.log('  - Ya se notificó recientemente');
            console.log('  - No hay correos configurados');
        }
        
    } catch (error) {
        console.error('❌ Error:', error);
    }
}

// 4. Verificar variables de entorno (desde el backend)
async function checkEnvVars() {
    console.log('🔍 Verificando variables de entorno...');
    
    try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/notificaciones/test-email', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                to: 'test@example.com',
                subject: 'Test',
                body: 'Test'
            })
        });
        
        const data = await response.json();
        
        if (!data.success && data.config_status) {
            console.log('🔧 Estado de variables SMTP:');
            Object.entries(data.config_status).forEach(([key, value]) => {
                console.log(`  ${key}: ${value ? '✅' : '❌'}`);
            });
        }
        
    } catch (error) {
        console.error('❌ Error verificando variables:', error);
    }
}

// Exportar funciones
window.testEmailSystem = {
    testEmailConfig,
    testNotificationCompletion,
    checkEnvVars
};

console.log('📧 Sistema de test de correo cargado. Usa:');
console.log('  window.testEmailSystem.testEmailConfig()');
console.log('  window.testEmailSystem.testNotificationCompletion()');
console.log('  window.testEmailSystem.checkEnvVars()');
console.log('');
console.log('⚠️ IMPORTANTE: Reemplaza "tu_correo_de_prueba@gmail.com" con tu correo real.');
