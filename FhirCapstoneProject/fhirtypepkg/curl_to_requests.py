import email
import http
import json


class FakeFilePointer:
    """
    Overview
    --------
    Mimics a file pointer for use when coercing a bytes response into a requests.Response
    """

    def __init__(self, content: bytes or str):
        self.content = content

    def readline(self, size: int or None = None) -> bytes or str:
        return self.content

    def close(self):
        pass


class FakeSocket:
    """
    Overview
    --------
    Mimics a socket for use when coercing a bytes response into a requests.Response

    All functions herein are meant to shadow those of an actual requests socket
    """

    def __init__(self, curl_response: bytes):
        """
        Takes in a bytes response from a curl subprocess and presents like a socket receiving data
        :param curl_response: bytes response from a curl subprocess
        """
        self.curl_response = curl_response

        # Split the headers and payload
        self.header, self.body = self.curl_response.split(b"\r\n\r\n")

        # Parse the header
        self.header = self.header.decode("utf-8")
        self.headers = self.header.split("\r\n")

        # Decode the output and parse it as JSON
        self.response_data = json.loads(self.body.decode("utf-8"))

    def makefile(self, mode: str, *args, **kwargs):
        binary = "b" in mode

        if binary:
            return FakeFilePointer(self.curl_response)
        else:
            return FakeFilePointer(self.curl_response.decode("utf-8"))

    def get_body(self):
        return self.body

    def get_http_version(self):
        http_string = self.headers[0].split(" ")[0]

        if http_string == "HTTP/1.1":
            return 11

        return http_string

    def get_status_code(self):
        return int(self.headers[0].split(" ")[1])

    def get_reason(self):
        return self.headers[0].split(" ", 2)[2]


class FakeHTTPResponse(http.client.HTTPResponse):
    """
    Wraps HTTPResponse to serve data from a curl subprocess so that it may be handled seamlessly as a
    requests.Response down the line
    """

    def __init__(self, socket: FakeSocket or None):
        if socket is None:
            self.status = self.code = self.status_code = 500
        else:
            http.client.HTTPResponse.__init__(self, socket)
            self.socket = socket

            self.chunk_left = None
            self.chunked = True
            self.code = socket.get_status_code()
            self.status = socket.get_status_code()
            self.reason = socket.get_reason()
            self.version = socket.get_http_version()
            self._content = socket.body

            header_builder = email.message.Message()
            _raw_headers = []
            for header in socket.headers[1:]:
                name, value = header.split(": ", 2)
                header_builder.set_param(param=name, value=value, header=name)
                _raw_headers.append((name, value))

            header_message = http.client.HTTPMessage(header_builder)

            # self.headers = header_message
            self.headers = _raw_headers
            self.msg = header_message
            self._ft_has_been_read = False

    def read(self, amount: int or None = None):
        if self._ft_has_been_read:
            return None

        self._ft_has_been_read = True
        return self.socket.get_body()
