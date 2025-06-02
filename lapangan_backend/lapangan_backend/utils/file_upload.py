import os
import uuid
import shutil
import logging
from pyramid.request import Request

log = logging.getLogger(__name__)

def save_uploaded_file(request: Request, field_name: str, upload_dir: str, allowed_extensions=None):
    """
    Save an uploaded file to the specified directory
    
    Args:
        request: The pyramid request object
        field_name: The name of the file field in the form
        upload_dir: The directory to save the file to
        allowed_extensions: List of allowed file extensions (e.g. ['.jpg', '.png'])
        
    Returns:
        The URL path to the saved file or None if there was an error
    """
    try:
        # Log request information for debugging
        log.info(f"Processing file upload. Field name: {field_name}")
        log.info(f"POST keys: {list(request.POST.keys())}")
        log.info(f"Files in request: {list(request.POST)}")
        
        # Check if the upload directory exists, create it if not
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir, exist_ok=True)
            log.info(f"Created upload directory: {upload_dir}")
        
        # Get the uploaded file
        file_obj = request.POST.get(field_name)
        log.info(f"File object type: {type(file_obj)}")
        
        if file_obj is None:
            log.error(f"No file found with field name: {field_name}")
            # Try to find any file-like object in the request
            for key in request.POST.keys():
                item = request.POST.get(key)
                log.info(f"Field {key} type: {type(item)}")
                if hasattr(item, 'filename'):
                    log.info(f"Found file-like object in field: {key}")
                    file_obj = item
                    log.info(f"Using file from field: {key} instead")
                    break
            
            if file_obj is None:
                return None
            
        if not hasattr(file_obj, 'filename'):
            log.error(f"File object has no filename attribute: {file_obj}")
            return None
        
        log.info(f"Uploaded filename: {file_obj.filename}")
        
        # Check file extension if allowed_extensions is provided
        if allowed_extensions:
            _, ext = os.path.splitext(file_obj.filename)
            ext_lower = ext.lower()
            log.info(f"File extension: {ext}, Lowercase: {ext_lower}")
            log.info(f"Checking if extension is allowed. Allowed extensions: {allowed_extensions}")
            
            # Convert all allowed extensions to lowercase for case-insensitive comparison
            allowed_lower = [e.lower() for e in allowed_extensions]
            log.info(f"Lowercase allowed extensions: {allowed_lower}")
            
            if ext_lower not in allowed_lower:
                log.error(f"Invalid file extension: {ext}. Allowed: {allowed_extensions}")
                return None
            else:
                log.info(f"File extension {ext_lower} is valid")
        
        # Generate a unique filename to prevent overwriting
        unique_filename = f"{uuid.uuid4()}{os.path.splitext(file_obj.filename)[1]}"
        file_path = os.path.join(upload_dir, unique_filename)
        log.info(f"Generated unique filename: {unique_filename}")
        
        # Save the file content directly to avoid permission issues with temp files
        try:
            log.info(f"Saving file to: {file_path}")
            with open(file_path, 'wb') as output_file:
                if hasattr(file_obj, 'file'):
                    # Read the content first, then write it
                    file_obj.file.seek(0)
                    file_content = file_obj.file.read()
                    output_file.write(file_content)
                    log.info(f"Successfully wrote {len(file_content)} bytes to {file_path}")
                else:
                    log.error("File object doesn't have 'file' attribute, cannot save")
                    return None
            
            # Return the relative URL path to the file
            image_url = f"/static/uploads/courts/{unique_filename}"
            log.info(f"File saved successfully. URL: {image_url}")
            return image_url
        except Exception as e:
            log.error(f"Error saving file: {str(e)}")
            return None
    except Exception as e:
        log.error(f"Error in save_uploaded_file: {str(e)}")
        return None
