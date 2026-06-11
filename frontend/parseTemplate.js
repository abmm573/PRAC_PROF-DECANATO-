const fs = require('fs');
const { parse } = require('@vue/compiler-dom');
const tpl = fs.readFileSync('src/components/EncargadoUsuarios.vue', 'utf-8');
const match = tpl.match(/<template>([\s\S]*)<\/template>/);
if (match) {
  try {
    parse(match[1]);
    console.log('parsed ok');
  } catch (e) {
    console.error('parse error:', e.message);
    console.error(e);
  }
} else {
  console.log('no template');
}
