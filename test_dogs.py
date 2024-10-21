import pytest
import requests


class YaUploader:
    base_endpoint = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token, path):
        self.token = token
        self.path = path

    def create_folder(self):
        response = requests.put(f'{YaUploader.base_endpoint}?path={self.path}', headers=self.headers)
        response.raise_for_status()

    def upload_photo(self, url_file, name):
        url = f'{YaUploader.base_endpoint}/upload'
        params = {"path": f'/{self.path}/{name}', 'url': url_file, "overwrite": "true"}
        response = requests.post(url, headers=self.headers, params=params)
        response.raise_for_status()
        self.wait_for_operation(response.json()['href'])

    def wait_for_operation(self, url):
        status = self.get_operation_status(url)
        while status == 'in-progress':
            status = self.get_operation_status(url)

    def get_operation_status(self, url):
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()['status']

    def delete_folder(self):
        response = requests.delete(f'{YaUploader.base_endpoint}?path={self.path}', headers=self.headers)
        response.raise_for_status()

    @property
    def headers(self):
        return {'Content-Type': 'application/json', 'Accept': 'application/json',
                'Authorization': f'OAuth {self.token}'}


class DogApi:
    base_endpoint = 'https://dog.ceo/api/breed'

    @staticmethod
    def get_sub_breeds(breed):
        response = requests.get(f'{DogApi.base_endpoint}/{breed}/list')
        response.raise_for_status()
        return response.json().get('message', [])

    @staticmethod
    def get_breed_random_image(breed, sub_breed=None):
        sub_breed_url_part = f"{sub_breed}/" if sub_breed else ""
        response = requests.get(f"{DogApi.base_endpoint}/{breed}/{sub_breed_url_part}images/random")
        response.raise_for_status()
        return response.json().get('message')

    @staticmethod
    def get_random_images(breed, sub_breeds):
        url_images = []
        if sub_breeds:
            for sub_breed in sub_breeds:
                url_images.append(DogApi.get_breed_random_image(breed, sub_breed))
        else:
            url_images.append(DogApi.get_breed_random_image(breed))
        return url_images


class TestDogLoader:
    yandex_client = YaUploader('AgAAAAAJtest_tokenxkUEdew', 'test_folder')

    @staticmethod
    def upload_dog(breed):
        sub_breeds = DogApi.get_sub_breeds(breed)
        urls = DogApi.get_random_images(breed, sub_breeds)
        for url in urls:
            part_name = url.split('/')
            name = '_'.join([part_name[-2], part_name[-1]])
            TestDogLoader.yandex_client.upload_photo(url, name)

    @staticmethod
    def get_files_from_disk():
        url_create = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
                   'Authorization': f'OAuth {TestDogLoader.yandex_client.token}'}
        response = requests.get(f'{url_create}?path=/{TestDogLoader.yandex_client.path}', headers=headers)
        response.raise_for_status()
        return response

    @staticmethod
    def check_response(files_info, breed, sub_breeds_count=1):
        assert files_info['type'] == "dir"
        assert files_info['name'] == "test_folder"

        items = files_info['_embedded']['items']
        assert len(items) == sub_breeds_count
        for item in items:
            assert item['type'] == 'file'
            assert item['name'].startswith(breed)

    @pytest.fixture(autouse=True)
    def setup(self, request):
        self.yandex_client.create_folder()

        def finalizer():
            self.yandex_client.delete_folder()

        request.addfinalizer(finalizer)

    @pytest.fixture(params=['doberman'])
    def breed_without_sub_breeds(self, request):
        self.upload_dog(request.param)
        return request.param

    @pytest.fixture(params=['bulldog', 'collie'])
    def breed_with_sub_breeds(self, request):
        self.upload_dog(request.param)
        return request.param, len(DogApi.get_sub_breeds(request.param))

    @pytest.fixture
    def uploaded_files_info(self):
        return self.get_files_from_disk().json()

    def test_upload_dog_without_sub_breeds(self, breed_without_sub_breeds, uploaded_files_info):
        TestDogLoader.check_response(uploaded_files_info, breed_without_sub_breeds)

    def test_upload_dog_with_sub_breeds(self, breed_with_sub_breeds, uploaded_files_info):
        breed_with_sub_breeds, sub_breeds_count = breed_with_sub_breeds

        TestDogLoader.check_response(uploaded_files_info, breed_with_sub_breeds, sub_breeds_count)
