from django.db import models

# Modelo de los tecnicos:
class Technical(models.Model):
	technical_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	date_hire = models.DateField()

	def __str__(self):
		return self.name


# Modelo de los clientes:
class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    direction = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    date_register = models.DateField()

    def __str__(self):
        return f"Client {self.client_id}"

# Modelo de los pedidos:
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    technical = models.ForeignKey(Technical, on_delete=models.SET_NULL, null=True, related_name='orders')
    total_euros = models.FloatField()
    date_register = models.CharField(max_length=50)  # Puedes usar DateField si prefieres

    def __str__(self):
        return f"Order {self.order_id}"


# Modelo de las impresoras:
class Printer(models.Model):
    printer_id = models.AutoField(primary_key=True)
    description = models.TextField()
    hours_use = models.IntegerField()
    last_change_nozzle = models.DateField()
    last_maintenance = models.DateField()
    technical_assigned = models.ForeignKey(Technical, on_delete=models.SET_NULL, null=True, related_name='printers')

    def __str__(self):
        return f"Printer {self.printer_id}"
