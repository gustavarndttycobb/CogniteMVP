import pytest
from unittest.mock import Mock
from app.domain.models import Facility, Documentation, FileReference
from app.services.facility_service import FacilityService
from app.services.documentation_service import DocumentationService

def test_list_facilities():
    mock_repo = Mock()
    mock_repo.list.return_value = [
        Facility(external_id="f1", space="s1", name="Facility 1"),
        Facility(external_id="f2", space="s1", name="Facility 2")
    ]
    
    service = FacilityService(mock_repo)
    facilities = service.list_facilities()
    
    assert len(facilities) == 2
    assert facilities[0].name == "Facility 1"
    mock_repo.list.assert_called_once()

def test_upsert_facility():
    mock_repo = Mock()
    facility = Facility(external_id="f1", space="s1", name="New Facility")
    mock_repo.upsert.return_value = facility
    
    service = FacilityService(mock_repo)
    result = service.upsert_facility(facility)
    
    assert result.name == "New Facility"
    mock_repo.upsert.assert_called_with(facility)

def test_upload_and_create_documentation():
    mock_doc_repo = Mock()
    mock_file_repo = Mock()
    
    # Mock return values
    mock_file_repo.upload_bytes.return_value = Mock(id=123, external_id="doc1_file")
    mock_doc_repo.upsert.return_value = Documentation(
        external_id="doc1", 
        space="s1", 
        name="Doc 1", 
        file=FileReference(external_id="doc1_file")
    )
    
    service = DocumentationService(mock_doc_repo, mock_file_repo)
    
    result = service.upload_and_create(
        content=b"content",
        filename="test.txt",
        mime_type="text/plain",
        doc_external_id="doc1",
        space="s1",
        name="Doc 1"
    )
    
    # Verify interactions
    mock_file_repo.upload_bytes.assert_called_once()
    mock_doc_repo.upsert.assert_called_once()
    
    # Verify logic
    assert result.external_id == "doc1"
    assert result.file.external_id == "doc1_file"
