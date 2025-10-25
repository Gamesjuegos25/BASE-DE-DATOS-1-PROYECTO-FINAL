# RUTAS BÁSICAS PARA MÓDULOS NUEVOS
# ==================================
# Agregar al final de app.py antes de if __name__ == '__main__'


# =================== RUTAS HERRAMIENTAS ===================

@app.route('/herramientas')
def listar_herramientas():
    """Listar herramientas"""
    return render_template('herramientas/listar.html', herramientas=[])

@app.route('/herramientas/crear', methods=['GET', 'POST'])
def crear_herramientas():
    """Crear herramienta"""
    if request.method == 'POST':
        flash('Funcionalidad en desarrollo', 'info')
        return redirect(url_for('listar_herramientas'))
    return render_template('herramientas/crear.html')

@app.route('/herramientas/<int:id>')
def ver_herramientas(id):
    """Ver herramienta"""
    return render_template('herramientas/detalle.html')

@app.route('/herramientas/<int:id>/editar', methods=['GET', 'POST'])  
def editar_herramientas(id):
    """Editar herramienta"""
    if request.method == 'POST':
        flash('Funcionalidad en desarrollo', 'info')
        return redirect(url_for('listar_herramientas'))
    return render_template('herramientas/editar.html')


# =================== RUTAS COMPRAS ===================

@app.route('/compras')
def listar_compras():
    """Listar compras"""
    return render_template('compras/listar.html', compras=[])

@app.route('/compras/crear', methods=['GET', 'POST'])
def crear_compras():
    """Crear compra"""
    if request.method == 'POST':
        flash('Funcionalidad en desarrollo', 'info')
        return redirect(url_for('listar_compras'))
    return render_template('compras/crear.html')

@app.route('/compras/<int:id>')
def ver_compras(id):
    """Ver compra"""
    return render_template('compras/detalle.html')

@app.route('/compras/<int:id>/editar', methods=['GET', 'POST'])  
def editar_compras(id):
    """Editar compra"""
    if request.method == 'POST':
        flash('Funcionalidad en desarrollo', 'info')
        return redirect(url_for('listar_compras'))
    return render_template('compras/editar.html')


# =================== RUTAS VENTAS ===================

@app.route('/ventas')
def listar_ventas():
    """Listar ventas"""
    return render_template('ventas/listar.html', ventas=[])

@app.route('/ventas/crear', methods=['GET', 'POST'])
def crear_ventas():
    """Crear venta"""
    if request.method == 'POST':
        flash('Funcionalidad en desarrollo', 'info')
        return redirect(url_for('listar_ventas'))
    return render_template('ventas/crear.html')

@app.route('/ventas/<int:id>')
def ver_ventas(id):
    """Ver venta"""
    return render_template('ventas/detalle.html')

@app.route('/ventas/<int:id>/editar', methods=['GET', 'POST'])  
def editar_ventas(id):
    """Editar venta"""
    if request.method == 'POST':
        flash('Funcionalidad en desarrollo', 'info')
        return redirect(url_for('listar_ventas'))
    return render_template('ventas/editar.html')


# =================== RUTAS PAGOS ===================

@app.route('/pagos')
def listar_pagos():
    """Listar pagos"""
    return render_template('pagos/listar.html', pagos=[])

@app.route('/pagos/crear', methods=['GET', 'POST'])
def crear_pagos():
    """Crear pago"""
    if request.method == 'POST':
        flash('Funcionalidad en desarrollo', 'info')
        return redirect(url_for('listar_pagos'))
    return render_template('pagos/crear.html')

@app.route('/pagos/<int:id>')
def ver_pagos(id):
    """Ver pago"""
    return render_template('pagos/detalle.html')

@app.route('/pagos/<int:id>/editar', methods=['GET', 'POST'])  
def editar_pagos(id):
    """Editar pago"""
    if request.method == 'POST':
        flash('Funcionalidad en desarrollo', 'info')
        return redirect(url_for('listar_pagos'))
    return render_template('pagos/editar.html')


# =================== RUTAS NOMINA ===================

@app.route('/nomina')
def listar_nomina():
    """Listar nomina"""
    return render_template('nomina/listar.html', nomina=[])

@app.route('/nomina/crear', methods=['GET', 'POST'])
def crear_nomina():
    """Crear nomin"""
    if request.method == 'POST':
        flash('Funcionalidad en desarrollo', 'info')
        return redirect(url_for('listar_nomina'))
    return render_template('nomina/crear.html')

@app.route('/nomina/<int:id>')
def ver_nomina(id):
    """Ver nomin"""
    return render_template('nomina/detalle.html')

@app.route('/nomina/<int:id>/editar', methods=['GET', 'POST'])  
def editar_nomina(id):
    """Editar nomin"""
    if request.method == 'POST':
        flash('Funcionalidad en desarrollo', 'info')
        return redirect(url_for('listar_nomina'))
    return render_template('nomina/editar.html')

