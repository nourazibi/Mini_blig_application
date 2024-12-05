from django.test import TestCase
from django.urls import reverse
from .models import BlogPost

# Create your tests here.

class BlogPostTests(TestCase):
    
    def test_create_blog_post(self):
        
        post_data = {'title': 'Test Post', 'content': 'This is a test content.'}
        response = self.client.post(reverse('create_post'), data=post_data)
        self.assertRedirects(response, reverse('post_list'))
        self.assertEqual(BlogPost.objects.count(), 1)
        self.assertEqual(BlogPost.objects.first().title, 'Test Post')


    def test_edit_blog_post(self):
        post = BlogPost.objects.create(title='Old Title', content='Old content.')
        
        edit_data = {'title': 'Updated Title', 'content': 'Updated content.'}
        response = self.client.post(reverse('edit_post', kwargs={'pk': post.pk}), data=edit_data)
        self.assertRedirects(response, reverse('post_detail', kwargs={'pk': post.pk}))
        post.refresh_from_db()
        self.assertEqual(post.title, 'Updated Title')
        self.assertEqual(post.content, 'Updated content.')


    def test_delete_blog_post(self):
        post = BlogPost.objects.create(title='Post to Delete', content='Content to be deleted.')
        
        response = self.client.post(reverse('delete_post', kwargs={'pk': post.pk}))
        self.assertRedirects(response, reverse('post_list'))
        self.assertEqual(BlogPost.objects.count(), 0)


    def test_add_comment(self):
        post = BlogPost.objects.create(title='Test Post', content='Content for commenting.')
        
        comment_data = {'author': 'Alice', 'text': 'Great post!'}
        response = self.client.post(reverse('add_comment', kwargs={'pk': post.pk}), data=comment_data)
        self.assertRedirects(response, reverse('post_detail', kwargs={'pk': post.pk}))
        self.assertEqual(post.comment_set.count(), 1)
        self.assertEqual(post.comment_set.first().author, 'Alice')
        self.assertEqual(post.comment_set.first().text, 'Great post!')


    def test_edit_comment(self):
        post = BlogPost.objects.create(title='Test Post', content='Content for editing comment.')
        comment = post.comment_set.create(author='Alice', text='Great post!')

        comment_data = {'author': 'Alice', 'text': 'Updated comment.'}
        response = self.client.post(reverse('edit_comment', kwargs={'post_pk': post.pk, 'comment_pk': comment.pk}), data=comment_data)
        self.assertRedirects(response, reverse('post_detail', kwargs={'pk': post.pk}))
        comment.refresh_from_db()
        self.assertEqual(comment.text, 'Updated comment.')


    def test_delete_comment(self):
        post = BlogPost.objects.create(title='Test Post', content='Content to delete comment.')
        comment = post.comment_set.create(author='Alice', text='Great post!')
        
        response = self.client.post(reverse('delete_comment', kwargs={'pk': comment.pk}))
        self.assertRedirects(response, reverse('post_detail', kwargs={'pk': post.pk}))
        self.assertEqual(post.comment_set.count(), 0)




