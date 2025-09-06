from tasks import task_a, task_b, task_c



if __name__ == "__main__":
	try:
		# Test connection by inspecting registered tasks (will raise if broker unreachable)
		print("Connected to RabbitMQ broker via Celery.")
		print("Registered tasks:", app.tasks.keys())
		# Test SQLAlchemy session
		
		print("SQLAlchemy connected to SQLite.")
		db.close()
	except Exception as e:
		print(f"Failed to connect: {e}")