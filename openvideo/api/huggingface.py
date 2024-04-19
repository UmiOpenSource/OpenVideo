from huggingface_hub import HfApi


def pull_file_from_hf(
    hf_token: str, hf_repo_id: str, filename: str, save_dir: str, 
    repo_type: str = "dataset", cache_dir: str = "hf_cache"
):
    hf_api = HfApi(token=hf_token)
    hf_api.hf_hub_download(
        repo_id=hf_repo_id,
        repo_type=repo_type,
        filename=filename,
        cache_dir=cache_dir,
        local_dir=save_dir,
        local_dir_use_symlinks=False
    )
  

def pull_repo_from_hf(
    hf_token: str, hf_repo_id: str, save_dir: str, 
    repo_type: str = "dataset", cache_dir: str = "hf_cache"
):
    hf_api = HfApi(token=hf_token)
    hf_api.snapshot_download(
        repo_id=hf_repo_id,
        repo_type=repo_type,
        cache_dir=cache_dir,
        local_dir=save_dir,
        local_dir_use_symlinks=False
    )


def push_file_to_hf(    
    hf_token: str, hf_repo_id: str, file_path: str, path_in_repo: str,
    repo_type: str = "dataset", commit_message="Add one file"
):
    hf_api = HfApi(token=hf_token)
    hf_api.upload_file(
        path_or_fileobj=file_path,
        path_in_repo=path_in_repo,
        repo_id=hf_repo_id,
        repo_type=repo_type,
        commit_message=commit_message
    )


def push_folder_to_hf(    
    hf_token: str, hf_repo_id: str, folder_path: str, path_in_repo: str,
    repo_type: str = "dataset", commit_message="Add one file"
):
    hf_api = HfApi(token=hf_token)
    hf_api.upload_folder(
        repo_id=hf_repo_id,
        folder_path=folder_path,
        path_in_repo=path_in_repo,
        commit_message=commit_message,
        repo_type=repo_type,
    )