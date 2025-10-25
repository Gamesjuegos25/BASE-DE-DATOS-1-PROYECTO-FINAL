#!/usr/bin/env python3
"""
ACTUALIZADOR DE RUTAS AUTOMÁTICO
================================
Añade las rutas faltantes para los módulos completados
"""

def actualizar_rutas_app():
    """Actualiza app.py con las rutas de los módulos faltantes"""
    
    # Rutas a agregar para cada módulo
    modulos_rutas = {
        'clientes': {
            'tabla': 'clientes',
            'campos': ['nombre', 'email', 'telefono', 'direccion', 'estado']
        },
        'herramientas': {
            'tabla': 'herramientas',
            'campos': ['nombre', 'tipo', 'marca', 'modelo', 'estado']
        },
        'compras': {
            'tabla': 'compras',
            'campos': ['proveedor_id', 'fecha_compra', 'total', 'estado']
        },
        'ventas': {
            'tabla': 'ventas',
            'campos': ['cliente_id', 'fecha_venta', 'total', 'estado']
        },
        'pagos': {
            'tabla': 'pagos',
            'campos': ['factura_id', 'fecha_pago', 'monto', 'metodo_pago']
        },
        'nomina': {
            'tabla': 'nomina',
            'campos': ['empleado_id', 'periodo', 'salario_base', 'deducciones', 'total']
        }
    }
    
    print("🔧 GENERANDO RUTAS PARA MÓDULOS FALTANTES...")
    print("=" * 50)
    
    # Generar código de rutas
    rutas_codigo = ""
    
    for modulo, config in modulos_rutas.items():
        tabla = config['tabla']
        campos = config['campos']
        campos_str = "', '".join(campos)
        
        rutas_codigo += f"""
# =================== RUTAS {modulo.upper()} ===================

@app.route('/{modulo}')
def listar_{modulo}():
    \"\"\"Listar todos los registros de {modulo}\"\"\"
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM {tabla} ORDER BY id DESC")
        {modulo} = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('{modulo}/listar.html', {modulo}={modulo})
    except Exception as e:
        flash(f'Error al cargar {modulo}: {{str(e)}}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/{modulo}/crear', methods=['GET', 'POST'])
def crear_{modulo}():
    \"\"\"Crear nuevo registro de {modulo}\"\"\"
    if request.method == 'POST':
        try:
            datos = {{}}
            for campo in ['{campos_str}']:
                datos[campo] = request.form.get(campo, '')
            
            conn = get_connection()
            cur = conn.cursor()
            
            campos_insert = ', '.join(datos.keys())
            valores_insert = ', '.join(['%s'] * len(datos))
            query = f"INSERT INTO {tabla} ({{campos_insert}}) VALUES ({{valores_insert}})"
            
            cur.execute(query, tuple(datos.values()))
            conn.commit()
            cur.close()
            conn.close()
            
            flash(f'{modulo.title().rstrip("s")} creado exitosamente', 'success')
            return redirect(url_for('listar_{modulo}'))
            
        except Exception as e:
            flash(f'Error al crear {modulo.rstrip("s")}: {{str(e)}}', 'error')
            return redirect(url_for('crear_{modulo}'))
    
    return render_template('{modulo}/crear.html')

@app.route('/{modulo}/<int:id>')
def ver_{modulo}(id):
    \"\"\"Ver detalles de un registro específico\"\"\"
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM {tabla} WHERE id = %s", (id,))
        {modulo.rstrip('s')} = cur.fetchone()
        cur.close()
        conn.close()
        
        if {modulo.rstrip('s')}:
            return render_template('{modulo}/detalle.html', {modulo.rstrip('s')}={modulo.rstrip('s')})
        else:
            flash('Registro no encontrado', 'error')
            return redirect(url_for('listar_{modulo}'))
            
    except Exception as e:
        flash(f'Error al cargar detalles: {{str(e)}}', 'error')
        return redirect(url_for('listar_{modulo}'))

@app.route('/{modulo}/<int:id>/editar', methods=['GET', 'POST'])
def editar_{modulo}(id):
    \"\"\"Editar registro existente\"\"\"
    if request.method == 'POST':
        try:
            datos = {{}}
            for campo in ['{campos_str}']:
                datos[campo] = request.form.get(campo, '')
            
            conn = get_connection()
            cur = conn.cursor()
            
            set_clause = ', '.join([f"{{k}} = %s" for k in datos.keys()])
            query = f"UPDATE {tabla} SET {{set_clause}} WHERE id = %s"
            valores = list(datos.values()) + [id]
            
            cur.execute(query, valores)
            conn.commit()
            cur.close()
            conn.close()
            
            flash(f'{modulo.title().rstrip("s")} actualizado exitosamente', 'success')
            return redirect(url_for('ver_{modulo}', id=id))
            
        except Exception as e:
            flash(f'Error al actualizar: {{str(e)}}', 'error')
    
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM {tabla} WHERE id = %s", (id,))
        {modulo.rstrip('s')} = cur.fetchone()
        cur.close()
        conn.close()
        
        if {modulo.rstrip('s')}:
            return render_template('{modulo}/editar.html', {modulo.rstrip('s')}={modulo.rstrip('s')})
        else:
            flash('Registro no encontrado', 'error')
            return redirect(url_for('listar_{modulo}'))
            
    except Exception as e:
        flash(f'Error al cargar registro: {{str(e)}}', 'error')
        return redirect(url_for('listar_{modulo}'))

@app.route('/{modulo}/<int:id>/eliminar', methods=['POST'])
def eliminar_{modulo}(id):
    \"\"\"Eliminar registro\"\"\"
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM {tabla} WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        
        flash(f'{modulo.title().rstrip("s")} eliminado exitosamente', 'success')
        return jsonify({{'success': True}})
        
    except Exception as e:
        return jsonify({{'success': False, 'error': str(e)}}), 500
"""
    
    print("✅ Código de rutas generado")
    
    # Generar archivo con las rutas
    with open('rutas_nuevas_modulos.py', 'w', encoding='utf-8') as f:
        f.write(f"""# RUTAS PARA MÓDULOS COMPLETADOS
# ================================
# Copiar e insertar al final de app.py antes de if __name__ == '__main__'

{rutas_codigo}

# =================== FIN RUTAS NUEVAS ===================
""")
    
    print("📄 Archivo 'rutas_nuevas_modulos.py' creado")
    print("💡 Para aplicar: copiar el contenido e insertar en app.py")
    
    # También crear verificación de templates base.html
    verificar_base_html()

def verificar_base_html():
    """Verifica que base.html tenga enlaces a los nuevos módulos"""
    print("\n🔍 VERIFICANDO ENLACES EN NAVEGACIÓN...")
    print("=" * 40)
    
    try:
        with open('templates/base.html', 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        modulos_nuevos = ['clientes', 'herramientas', 'compras', 'ventas', 'pagos', 'nomina']
        enlaces_faltantes = []
        
        for modulo in modulos_nuevos:
            if f"listar_{modulo}" not in contenido:
                enlaces_faltantes.append(modulo)
        
        if enlaces_faltantes:
            print(f"⚠️  Enlaces faltantes en navegación: {', '.join(enlaces_faltantes)}")
            
            # Generar enlaces para base.html
            enlaces_html = ""
            for modulo in enlaces_faltantes:
                enlaces_html += f"""                        <li><a href="{{{{ url_for('listar_{modulo}') }}}}" class="nav-link"><i class="fas fa-list"></i> {modulo.title()}</a></li>
"""
            
            print("💡 Agregar estos enlaces al menú de navegación en base.html:")
            print(enlaces_html)
        else:
            print("✅ Todos los enlaces están presentes en la navegación")
            
    except FileNotFoundError:
        print("❌ No se pudo encontrar templates/base.html")

def main():
    """Función principal"""
    actualizar_rutas_app()
    
    print("\n🎯 RESUMEN DE ACCIONES REQUERIDAS:")
    print("=" * 40)
    print("1. ✅ Templates creados para todos los módulos")
    print("2. ✅ CSS unificado implementado") 
    print("3. ⏳ Agregar rutas de rutas_nuevas_modulos.py a app.py")
    print("4. ⏳ Actualizar enlaces de navegación en base.html")
    print("5. ⏳ Verificar funcionamiento de nuevos módulos")

if __name__ == "__main__":
    main()