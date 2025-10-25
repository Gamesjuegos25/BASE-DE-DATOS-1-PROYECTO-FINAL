# RUTAS PARA MÓDULOS COMPLETADOS
# ================================
# Copiar e insertar al final de app.py antes de if __name__ == '__main__'


# =================== RUTAS CLIENTES ===================

@app.route('/clientes')
def listar_clientes():
    """Listar todos los registros de clientes"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM clientes ORDER BY id DESC")
        clientes = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('clientes/listar.html', clientes=clientes)
    except Exception as e:
        flash(f'Error al cargar clientes: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/clientes/crear', methods=['GET', 'POST'])
def crear_clientes():
    """Crear nuevo registro de clientes"""
    if request.method == 'POST':
        try:
            datos = {}
            for campo in ['nombre', 'email', 'telefono', 'direccion', 'estado']:
                datos[campo] = request.form.get(campo, '')
            
            conn = get_connection()
            cur = conn.cursor()
            
            campos_insert = ', '.join(datos.keys())
            valores_insert = ', '.join(['%s'] * len(datos))
            query = f"INSERT INTO clientes ({campos_insert}) VALUES ({valores_insert})"
            
            cur.execute(query, tuple(datos.values()))
            conn.commit()
            cur.close()
            conn.close()
            
            flash(f'Cliente creado exitosamente', 'success')
            return redirect(url_for('listar_clientes'))
            
        except Exception as e:
            flash(f'Error al crear cliente: {str(e)}', 'error')
            return redirect(url_for('crear_clientes'))
    
    return render_template('clientes/crear.html')

@app.route('/clientes/<int:id>')
def ver_clientes(id):
    """Ver detalles de un registro específico"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM clientes WHERE id = %s", (id,))
        cliente = cur.fetchone()
        cur.close()
        conn.close()
        
        if cliente:
            return render_template('clientes/detalle.html', cliente=cliente)
        else:
            flash('Registro no encontrado', 'error')
            return redirect(url_for('listar_clientes'))
            
    except Exception as e:
        flash(f'Error al cargar detalles: {str(e)}', 'error')
        return redirect(url_for('listar_clientes'))

@app.route('/clientes/<int:id>/editar', methods=['GET', 'POST'])
def editar_clientes(id):
    """Editar registro existente"""
    if request.method == 'POST':
        try:
            datos = {}
            for campo in ['nombre', 'email', 'telefono', 'direccion', 'estado']:
                datos[campo] = request.form.get(campo, '')
            
            conn = get_connection()
            cur = conn.cursor()
            
            set_clause = ', '.join([f"{k} = %s" for k in datos.keys()])
            query = f"UPDATE clientes SET {set_clause} WHERE id = %s"
            valores = list(datos.values()) + [id]
            
            cur.execute(query, valores)
            conn.commit()
            cur.close()
            conn.close()
            
            flash(f'Cliente actualizado exitosamente', 'success')
            return redirect(url_for('ver_clientes', id=id))
            
        except Exception as e:
            flash(f'Error al actualizar: {str(e)}', 'error')
    
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM clientes WHERE id = %s", (id,))
        cliente = cur.fetchone()
        cur.close()
        conn.close()
        
        if cliente:
            return render_template('clientes/editar.html', cliente=cliente)
        else:
            flash('Registro no encontrado', 'error')
            return redirect(url_for('listar_clientes'))
            
    except Exception as e:
        flash(f'Error al cargar registro: {str(e)}', 'error')
        return redirect(url_for('listar_clientes'))

@app.route('/clientes/<int:id>/eliminar', methods=['POST'])
def eliminar_clientes(id):
    """Eliminar registro"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM clientes WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        
        flash(f'Cliente eliminado exitosamente', 'success')
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# =================== RUTAS HERRAMIENTAS ===================

@app.route('/herramientas')
def listar_herramientas():
    """Listar todos los registros de herramientas"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM herramientas ORDER BY id DESC")
        herramientas = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('herramientas/listar.html', herramientas=herramientas)
    except Exception as e:
        flash(f'Error al cargar herramientas: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/herramientas/crear', methods=['GET', 'POST'])
def crear_herramientas():
    """Crear nuevo registro de herramientas"""
    if request.method == 'POST':
        try:
            datos = {}
            for campo in ['nombre', 'tipo', 'marca', 'modelo', 'estado']:
                datos[campo] = request.form.get(campo, '')
            
            conn = get_connection()
            cur = conn.cursor()
            
            campos_insert = ', '.join(datos.keys())
            valores_insert = ', '.join(['%s'] * len(datos))
            query = f"INSERT INTO herramientas ({campos_insert}) VALUES ({valores_insert})"
            
            cur.execute(query, tuple(datos.values()))
            conn.commit()
            cur.close()
            conn.close()
            
            flash(f'Herramienta creado exitosamente', 'success')
            return redirect(url_for('listar_herramientas'))
            
        except Exception as e:
            flash(f'Error al crear herramienta: {str(e)}', 'error')
            return redirect(url_for('crear_herramientas'))
    
    return render_template('herramientas/crear.html')

@app.route('/herramientas/<int:id>')
def ver_herramientas(id):
    """Ver detalles de un registro específico"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM herramientas WHERE id = %s", (id,))
        herramienta = cur.fetchone()
        cur.close()
        conn.close()
        
        if herramienta:
            return render_template('herramientas/detalle.html', herramienta=herramienta)
        else:
            flash('Registro no encontrado', 'error')
            return redirect(url_for('listar_herramientas'))
            
    except Exception as e:
        flash(f'Error al cargar detalles: {str(e)}', 'error')
        return redirect(url_for('listar_herramientas'))

@app.route('/herramientas/<int:id>/editar', methods=['GET', 'POST'])
def editar_herramientas(id):
    """Editar registro existente"""
    if request.method == 'POST':
        try:
            datos = {}
            for campo in ['nombre', 'tipo', 'marca', 'modelo', 'estado']:
                datos[campo] = request.form.get(campo, '')
            
            conn = get_connection()
            cur = conn.cursor()
            
            set_clause = ', '.join([f"{k} = %s" for k in datos.keys()])
            query = f"UPDATE herramientas SET {set_clause} WHERE id = %s"
            valores = list(datos.values()) + [id]
            
            cur.execute(query, valores)
            conn.commit()
            cur.close()
            conn.close()
            
            flash(f'Herramienta actualizado exitosamente', 'success')
            return redirect(url_for('ver_herramientas', id=id))
            
        except Exception as e:
            flash(f'Error al actualizar: {str(e)}', 'error')
    
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM herramientas WHERE id = %s", (id,))
        herramienta = cur.fetchone()
        cur.close()
        conn.close()
        
        if herramienta:
            return render_template('herramientas/editar.html', herramienta=herramienta)
        else:
            flash('Registro no encontrado', 'error')
            return redirect(url_for('listar_herramientas'))
            
    except Exception as e:
        flash(f'Error al cargar registro: {str(e)}', 'error')
        return redirect(url_for('listar_herramientas'))

@app.route('/herramientas/<int:id>/eliminar', methods=['POST'])
def eliminar_herramientas(id):
    """Eliminar registro"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM herramientas WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        
        flash(f'Herramienta eliminado exitosamente', 'success')
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# =================== RUTAS COMPRAS ===================

@app.route('/compras')
def listar_compras():
    """Listar todos los registros de compras"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM compras ORDER BY id DESC")
        compras = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('compras/listar.html', compras=compras)
    except Exception as e:
        flash(f'Error al cargar compras: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/compras/crear', methods=['GET', 'POST'])
def crear_compras():
    """Crear nuevo registro de compras"""
    if request.method == 'POST':
        try:
            datos = {}
            for campo in ['proveedor_id', 'fecha_compra', 'total', 'estado']:
                datos[campo] = request.form.get(campo, '')
            
            conn = get_connection()
            cur = conn.cursor()
            
            campos_insert = ', '.join(datos.keys())
            valores_insert = ', '.join(['%s'] * len(datos))
            query = f"INSERT INTO compras ({campos_insert}) VALUES ({valores_insert})"
            
            cur.execute(query, tuple(datos.values()))
            conn.commit()
            cur.close()
            conn.close()
            
            flash(f'Compra creado exitosamente', 'success')
            return redirect(url_for('listar_compras'))
            
        except Exception as e:
            flash(f'Error al crear compra: {str(e)}', 'error')
            return redirect(url_for('crear_compras'))
    
    return render_template('compras/crear.html')

@app.route('/compras/<int:id>')
def ver_compras(id):
    """Ver detalles de un registro específico"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM compras WHERE id = %s", (id,))
        compra = cur.fetchone()
        cur.close()
        conn.close()
        
        if compra:
            return render_template('compras/detalle.html', compra=compra)
        else:
            flash('Registro no encontrado', 'error')
            return redirect(url_for('listar_compras'))
            
    except Exception as e:
        flash(f'Error al cargar detalles: {str(e)}', 'error')
        return redirect(url_for('listar_compras'))

@app.route('/compras/<int:id>/editar', methods=['GET', 'POST'])
def editar_compras(id):
    """Editar registro existente"""
    if request.method == 'POST':
        try:
            datos = {}
            for campo in ['proveedor_id', 'fecha_compra', 'total', 'estado']:
                datos[campo] = request.form.get(campo, '')
            
            conn = get_connection()
            cur = conn.cursor()
            
            set_clause = ', '.join([f"{k} = %s" for k in datos.keys()])
            query = f"UPDATE compras SET {set_clause} WHERE id = %s"
            valores = list(datos.values()) + [id]
            
            cur.execute(query, valores)
            conn.commit()
            cur.close()
            conn.close()
            
            flash(f'Compra actualizado exitosamente', 'success')
            return redirect(url_for('ver_compras', id=id))
            
        except Exception as e:
            flash(f'Error al actualizar: {str(e)}', 'error')
    
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM compras WHERE id = %s", (id,))
        compra = cur.fetchone()
        cur.close()
        conn.close()
        
        if compra:
            return render_template('compras/editar.html', compra=compra)
        else:
            flash('Registro no encontrado', 'error')
            return redirect(url_for('listar_compras'))
            
    except Exception as e:
        flash(f'Error al cargar registro: {str(e)}', 'error')
        return redirect(url_for('listar_compras'))

@app.route('/compras/<int:id>/eliminar', methods=['POST'])
def eliminar_compras(id):
    """Eliminar registro"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM compras WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        
        flash(f'Compra eliminado exitosamente', 'success')
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# =================== RUTAS VENTAS ===================

@app.route('/ventas')
def listar_ventas():
    """Listar todos los registros de ventas"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM ventas ORDER BY id DESC")
        ventas = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('ventas/listar.html', ventas=ventas)
    except Exception as e:
        flash(f'Error al cargar ventas: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/ventas/crear', methods=['GET', 'POST'])
def crear_ventas():
    """Crear nuevo registro de ventas"""
    if request.method == 'POST':
        try:
            datos = {}
            for campo in ['cliente_id', 'fecha_venta', 'total', 'estado']:
                datos[campo] = request.form.get(campo, '')
            
            conn = get_connection()
            cur = conn.cursor()
            
            campos_insert = ', '.join(datos.keys())
            valores_insert = ', '.join(['%s'] * len(datos))
            query = f"INSERT INTO ventas ({campos_insert}) VALUES ({valores_insert})"
            
            cur.execute(query, tuple(datos.values()))
            conn.commit()
            cur.close()
            conn.close()
            
            flash(f'Venta creado exitosamente', 'success')
            return redirect(url_for('listar_ventas'))
            
        except Exception as e:
            flash(f'Error al crear venta: {str(e)}', 'error')
            return redirect(url_for('crear_ventas'))
    
    return render_template('ventas/crear.html')

@app.route('/ventas/<int:id>')
def ver_ventas(id):
    """Ver detalles de un registro específico"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM ventas WHERE id = %s", (id,))
        venta = cur.fetchone()
        cur.close()
        conn.close()
        
        if venta:
            return render_template('ventas/detalle.html', venta=venta)
        else:
            flash('Registro no encontrado', 'error')
            return redirect(url_for('listar_ventas'))
            
    except Exception as e:
        flash(f'Error al cargar detalles: {str(e)}', 'error')
        return redirect(url_for('listar_ventas'))

@app.route('/ventas/<int:id>/editar', methods=['GET', 'POST'])
def editar_ventas(id):
    """Editar registro existente"""
    if request.method == 'POST':
        try:
            datos = {}
            for campo in ['cliente_id', 'fecha_venta', 'total', 'estado']:
                datos[campo] = request.form.get(campo, '')
            
            conn = get_connection()
            cur = conn.cursor()
            
            set_clause = ', '.join([f"{k} = %s" for k in datos.keys()])
            query = f"UPDATE ventas SET {set_clause} WHERE id = %s"
            valores = list(datos.values()) + [id]
            
            cur.execute(query, valores)
            conn.commit()
            cur.close()
            conn.close()
            
            flash(f'Venta actualizado exitosamente', 'success')
            return redirect(url_for('ver_ventas', id=id))
            
        except Exception as e:
            flash(f'Error al actualizar: {str(e)}', 'error')
    
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM ventas WHERE id = %s", (id,))
        venta = cur.fetchone()
        cur.close()
        conn.close()
        
        if venta:
            return render_template('ventas/editar.html', venta=venta)
        else:
            flash('Registro no encontrado', 'error')
            return redirect(url_for('listar_ventas'))
            
    except Exception as e:
        flash(f'Error al cargar registro: {str(e)}', 'error')
        return redirect(url_for('listar_ventas'))

@app.route('/ventas/<int:id>/eliminar', methods=['POST'])
def eliminar_ventas(id):
    """Eliminar registro"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM ventas WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        
        flash(f'Venta eliminado exitosamente', 'success')
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# =================== RUTAS PAGOS ===================

@app.route('/pagos')
def listar_pagos():
    """Listar todos los registros de pagos"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM pagos ORDER BY id DESC")
        pagos = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('pagos/listar.html', pagos=pagos)
    except Exception as e:
        flash(f'Error al cargar pagos: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/pagos/crear', methods=['GET', 'POST'])
def crear_pagos():
    """Crear nuevo registro de pagos"""
    if request.method == 'POST':
        try:
            datos = {}
            for campo in ['factura_id', 'fecha_pago', 'monto', 'metodo_pago']:
                datos[campo] = request.form.get(campo, '')
            
            conn = get_connection()
            cur = conn.cursor()
            
            campos_insert = ', '.join(datos.keys())
            valores_insert = ', '.join(['%s'] * len(datos))
            query = f"INSERT INTO pagos ({campos_insert}) VALUES ({valores_insert})"
            
            cur.execute(query, tuple(datos.values()))
            conn.commit()
            cur.close()
            conn.close()
            
            flash(f'Pago creado exitosamente', 'success')
            return redirect(url_for('listar_pagos'))
            
        except Exception as e:
            flash(f'Error al crear pago: {str(e)}', 'error')
            return redirect(url_for('crear_pagos'))
    
    return render_template('pagos/crear.html')

@app.route('/pagos/<int:id>')
def ver_pagos(id):
    """Ver detalles de un registro específico"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM pagos WHERE id = %s", (id,))
        pago = cur.fetchone()
        cur.close()
        conn.close()
        
        if pago:
            return render_template('pagos/detalle.html', pago=pago)
        else:
            flash('Registro no encontrado', 'error')
            return redirect(url_for('listar_pagos'))
            
    except Exception as e:
        flash(f'Error al cargar detalles: {str(e)}', 'error')
        return redirect(url_for('listar_pagos'))

@app.route('/pagos/<int:id>/editar', methods=['GET', 'POST'])
def editar_pagos(id):
    """Editar registro existente"""
    if request.method == 'POST':
        try:
            datos = {}
            for campo in ['factura_id', 'fecha_pago', 'monto', 'metodo_pago']:
                datos[campo] = request.form.get(campo, '')
            
            conn = get_connection()
            cur = conn.cursor()
            
            set_clause = ', '.join([f"{k} = %s" for k in datos.keys()])
            query = f"UPDATE pagos SET {set_clause} WHERE id = %s"
            valores = list(datos.values()) + [id]
            
            cur.execute(query, valores)
            conn.commit()
            cur.close()
            conn.close()
            
            flash(f'Pago actualizado exitosamente', 'success')
            return redirect(url_for('ver_pagos', id=id))
            
        except Exception as e:
            flash(f'Error al actualizar: {str(e)}', 'error')
    
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM pagos WHERE id = %s", (id,))
        pago = cur.fetchone()
        cur.close()
        conn.close()
        
        if pago:
            return render_template('pagos/editar.html', pago=pago)
        else:
            flash('Registro no encontrado', 'error')
            return redirect(url_for('listar_pagos'))
            
    except Exception as e:
        flash(f'Error al cargar registro: {str(e)}', 'error')
        return redirect(url_for('listar_pagos'))

@app.route('/pagos/<int:id>/eliminar', methods=['POST'])
def eliminar_pagos(id):
    """Eliminar registro"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM pagos WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        
        flash(f'Pago eliminado exitosamente', 'success')
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# =================== RUTAS NOMINA ===================

@app.route('/nomina')
def listar_nomina():
    """Listar todos los registros de nomina"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM nomina ORDER BY id DESC")
        nomina = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('nomina/listar.html', nomina=nomina)
    except Exception as e:
        flash(f'Error al cargar nomina: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/nomina/crear', methods=['GET', 'POST'])
def crear_nomina():
    """Crear nuevo registro de nomina"""
    if request.method == 'POST':
        try:
            datos = {}
            for campo in ['empleado_id', 'periodo', 'salario_base', 'deducciones', 'total']:
                datos[campo] = request.form.get(campo, '')
            
            conn = get_connection()
            cur = conn.cursor()
            
            campos_insert = ', '.join(datos.keys())
            valores_insert = ', '.join(['%s'] * len(datos))
            query = f"INSERT INTO nomina ({campos_insert}) VALUES ({valores_insert})"
            
            cur.execute(query, tuple(datos.values()))
            conn.commit()
            cur.close()
            conn.close()
            
            flash(f'Nomina creado exitosamente', 'success')
            return redirect(url_for('listar_nomina'))
            
        except Exception as e:
            flash(f'Error al crear nomina: {str(e)}', 'error')
            return redirect(url_for('crear_nomina'))
    
    return render_template('nomina/crear.html')

@app.route('/nomina/<int:id>')
def ver_nomina(id):
    """Ver detalles de un registro específico"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM nomina WHERE id = %s", (id,))
        nomina = cur.fetchone()
        cur.close()
        conn.close()
        
        if nomina:
            return render_template('nomina/detalle.html', nomina=nomina)
        else:
            flash('Registro no encontrado', 'error')
            return redirect(url_for('listar_nomina'))
            
    except Exception as e:
        flash(f'Error al cargar detalles: {str(e)}', 'error')
        return redirect(url_for('listar_nomina'))

@app.route('/nomina/<int:id>/editar', methods=['GET', 'POST'])
def editar_nomina(id):
    """Editar registro existente"""
    if request.method == 'POST':
        try:
            datos = {}
            for campo in ['empleado_id', 'periodo', 'salario_base', 'deducciones', 'total']:
                datos[campo] = request.form.get(campo, '')
            
            conn = get_connection()
            cur = conn.cursor()
            
            set_clause = ', '.join([f"{k} = %s" for k in datos.keys()])
            query = f"UPDATE nomina SET {set_clause} WHERE id = %s"
            valores = list(datos.values()) + [id]
            
            cur.execute(query, valores)
            conn.commit()
            cur.close()
            conn.close()
            
            flash(f'Nomina actualizado exitosamente', 'success')
            return redirect(url_for('ver_nomina', id=id))
            
        except Exception as e:
            flash(f'Error al actualizar: {str(e)}', 'error')
    
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM nomina WHERE id = %s", (id,))
        nomina = cur.fetchone()
        cur.close()
        conn.close()
        
        if nomina:
            return render_template('nomina/editar.html', nomina=nomina)
        else:
            flash('Registro no encontrado', 'error')
            return redirect(url_for('listar_nomina'))
            
    except Exception as e:
        flash(f'Error al cargar registro: {str(e)}', 'error')
        return redirect(url_for('listar_nomina'))

@app.route('/nomina/<int:id>/eliminar', methods=['POST'])
def eliminar_nomina(id):
    """Eliminar registro"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM nomina WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        
        flash(f'Nomina eliminado exitosamente', 'success')
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# =================== FIN RUTAS NUEVAS ===================
