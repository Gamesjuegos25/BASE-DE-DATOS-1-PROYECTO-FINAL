-- Mejora mínima necesaria para poder hacer factura 
ALTER TABLE CONTRATOS 
ADD COLUMN numero_factura VARCHAR(50),
ADD COLUMN fecha_emision_factura DATE,
ADD COLUMN estado_factura VARCHAR(20) DEFAULT 'PENDIENTE',
ADD COLUMN subtotal_factura DECIMAL(12,2),
ADD COLUMN iva_factura DECIMAL(12,2),
ADD COLUMN total_factura DECIMAL(12,2);

select * from CONTRATOS