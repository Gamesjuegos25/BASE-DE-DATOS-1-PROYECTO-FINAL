from database import get_contratos_safe, get_facturas_safe, get_obras_safe

print("\n🔍 VERIFICANDO DATOS EN LA BASE DE DATOS")
print("=" * 60)

# Verificar contratos
print("\n📋 CONTRATOS:")
contratos = get_contratos_safe()
print(f"   Total: {len(contratos)}")
if contratos:
    print("\n   Primeros 3 contratos:")
    for i, c in enumerate(contratos[:3], 1):
        print(f"\n   {i}. ID: {c.get('id_contrato')}")
        print(f"      Fecha inicio: {c.get('fecha_inicio_contrato')}")
        print(f"      Tipo pago: {c.get('tipo_pago_contrato', 'N/A')}")
        print(f"      Obra: {c.get('nombre_obra', 'Sin obra')}")
else:
    print("   ❌ No hay contratos en la base de datos")

# Verificar obras
print("\n🏗️  OBRAS:")
obras = get_obras_safe()
print(f"   Total: {len(obras)}")
if obras:
    print("\n   Primeras 3 obras:")
    for i, o in enumerate(obras[:3], 1):
        print(f"\n   {i}. ID: {o.get('id_obra')}")
        print(f"      Nombre: {o.get('nombre_obra')}")
else:
    print("   ❌ No hay obras en la base de datos")

# Verificar facturas
print("\n💰 FACTURAS:")
facturas = get_facturas_safe()
print(f"   Total: {len(facturas)}")
if facturas:
    print("\n   Primeras 3 facturas:")
    for i, f in enumerate(facturas[:3], 1):
        print(f"\n   {i}. ID: {f.get('id_factura')}")
        print(f"      Número: {f.get('numero_factura')}")
        print(f"      Cliente: {f.get('nombre_cliente', 'Sin cliente')}")
        print(f"      Total: ${f.get('total', 0):,.2f}")
else:
    print("   ❌ No hay facturas en la base de datos")

print("\n" + "=" * 60)
print("✅ VERIFICACIÓN COMPLETADA\n")
