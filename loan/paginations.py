from rest_framework import pagination


class CustomPagination(pagination.PageNumberPagination):
    page_size = 25
    max_page_size = 50



