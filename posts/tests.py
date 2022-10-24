from django.urls import reverse
from django.test import TestCase



class PostsUrlsTest(TestCase):
    def test_url_index_esta_correta_e_retorna_200(self):
        url = reverse('posts:index')
        url_status = self.client.get(reverse('posts:index'))

        self.assertEqual(url, '/')
        self.assertEqual(url_status.status_code, 200)

    def test_template_de_index_esta_correto(self):
        resp = self.client.get(reverse('posts:index'))

        self.assertTemplateUsed(resp, 'posts/index.html')
    
    

