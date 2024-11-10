from starlette.middleware.base import BaseHTTPMiddleware
import logging
import time


class LogRequestsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        logger = logging.getLogger("api_logs")

        # Registra la información de la solicitud (URL, método)
        start_time = time.time()
        logger.info(f"Request: {request.method} {request.url.path}")

        response = await call_next(request)  # Procesa la solicitud

        # Tiempo que tarda la solicitud en completarse
        process_time = time.time() - start_time
        formatted_process_time = "{:.2f}".format(
            process_time * 1000
        )  # Convertir a milisegundos

        # Registra el estado de la respuesta y el tiempo de proceso
        logger.info(
            f"Response status: {response.status_code} | Process time: {formatted_process_time} ms"
        )

        return response
