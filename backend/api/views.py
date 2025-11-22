from rest_framework.views import APIView
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import Dataset
from .serializers import DatasetSerializer
from .utils import parse_csv_and_summary, generate_pdf_report

class UploadCSVView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        f = request.FILES.get('file')
        if not f:
            return Response({"error":"No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        ds = Dataset.objects.create(file=f, original_filename=f.name)
        summary, df = parse_csv_and_summary(ds.file.path)
        ds.set_summary(summary)
        pdf_file = generate_pdf_report(summary, df, title=f"Report: {ds.original_filename}")
        ds.pdf_report.save(f"{ds.id}_report.pdf", pdf_file)
        all_ds = Dataset.objects.order_by('-uploaded_at')
        if all_ds.count() > 5:
            for old in all_ds[5:]:
                try:
                    old.file.delete(save=False)
                    if old.pdf_report:
                        old.pdf_report.delete(save=False)
                    old.delete()
                except Exception:
                    pass
        serializer = DatasetSerializer(ds)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DatasetListView(generics.ListAPIView):
    serializer_class = DatasetSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Dataset.objects.order_by('-uploaded_at')[:5]

class DatasetDetailView(generics.RetrieveAPIView):
    serializer_class = DatasetSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Dataset.objects.all()

class SummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk):
        try:
            ds = Dataset.objects.get(pk=pk)
        except Dataset.DoesNotExist:
            return Response(status=404)
        return Response(ds.get_summary())

class ReportDownloadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk):
        try:
            ds = Dataset.objects.get(pk=pk)
        except Dataset.DoesNotExist:
            return Response(status=404)
        if not ds.pdf_report:
            return Response({"error":"Report not found"}, status=404)
        return Response({'report_url': request.build_absolute_uri(ds.pdf_report.url)})
