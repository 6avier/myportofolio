import json
import logging

from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from main.models import Experience, Education, Project
from main.permissions import EDITOR_GROUP


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Frontend Developer VETO",
            description="Membangun antarmuka aplikasi compliance logistik.",
            category="part-time",
        )
        self.education = Education.objects.create(
            institution="Universitas Indonesia",
            program="Information Systems",
            start_year=2025,
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")
        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Frontend Developer VETO")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Ongoing")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))
        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))
        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Completed")
        self.assertNotContains(response, "Ongoing")

    def test_education_page(self):
        response = self.client.get(reverse("main:show_education"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")
        self.assertContains(response, self.education.institution)
        self.assertContains(response, self.education.program)

    def test_empty_education_page(self):
        Education.objects.all().delete()
        response = self.client.get(reverse("main:show_education"))
        self.assertContains(response, "Belum ada riwayat pendidikan yang ditambahkan.")

    def test_education_ongoing_vs_completed(self):
        response = self.client.get(reverse("main:show_education"))
        self.assertContains(response, "2025 - Current")

        self.education.end_year = 2029
        self.education.save()
        response = self.client.get(reverse("main:show_education"))
        self.assertContains(response, "2025 - 2029")


PASSWORD = "S3cure-pass-for-tests!"


class RoleTestCase(TestCase):
    """Base class: one experience, plus a regular user, an editor and an owner."""

    def setUp(self):
        logging.disable(logging.WARNING)  # keep expected 403 warnings out of test output
        self.addCleanup(logging.disable, logging.NOTSET)

        self.experience = Experience.objects.create(
            title="Digital Marketing COMPFEST",
            description="Produced short-form video campaigns.",
        )
        self.regular = User.objects.create_user("regular", password=PASSWORD)
        self.editor = User.objects.create_user("editor", password=PASSWORD)
        self.editor.groups.add(Group.objects.create(name=EDITOR_GROUP))
        self.owner = User.objects.create_superuser("owner", password=PASSWORD)

        self.create_url = reverse("main:create_experience")
        self.update_url = reverse("main:update_experience", args=[self.experience.id])
        self.delete_url = reverse("main:delete_experience", args=[self.experience.id])
        self.star_url = reverse("main:toggle_star_experience", args=[self.experience.id])

    def login_as(self, user):
        self.assertTrue(self.client.login(username=user.username, password=PASSWORD))

    def form_data(self, title="Edited title"):
        return {"title": title, "description": "Edited description", "category": "research"}


class ExperiencePermissionTest(RoleTestCase):
    def test_visitor_is_redirected_to_login_for_every_action(self):
        for url in (self.create_url, self.update_url, self.delete_url, self.star_url):
            response = self.client.post(url, self.form_data())
            self.assertRedirects(response, f"/login/?next={url}", fetch_redirect_response=False)
        self.assertTrue(Experience.objects.filter(pk=self.experience.pk, title="Digital Marketing COMPFEST").exists())

    def test_regular_user_cannot_create_update_or_delete(self):
        self.login_as(self.regular)
        self.assertEqual(self.client.get(self.create_url).status_code, 403)
        self.assertEqual(self.client.post(self.create_url, self.form_data()).status_code, 403)
        self.assertEqual(self.client.post(self.update_url, self.form_data()).status_code, 403)
        self.assertEqual(self.client.post(self.delete_url).status_code, 403)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Digital Marketing COMPFEST")
        self.assertEqual(Experience.objects.count(), 1)

    def test_editor_can_update_but_not_create_or_delete(self):
        self.login_as(self.editor)
        self.assertEqual(self.client.get(self.update_url).status_code, 200)
        self.assertRedirects(
            self.client.post(self.update_url, self.form_data("Updated by editor")),
            reverse("main:show_experience"),
        )
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Updated by editor")

        self.assertEqual(self.client.post(self.create_url, self.form_data()).status_code, 403)
        self.assertEqual(self.client.post(self.delete_url).status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)

    def test_owner_can_create_update_and_delete(self):
        self.login_as(self.owner)
        self.assertRedirects(self.client.post(self.create_url, self.form_data("Brand new")), reverse("main:show_experience"))
        self.assertTrue(Experience.objects.filter(title="Brand new").exists())

        self.client.post(self.update_url, self.form_data("Owner edit"))
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Owner edit")

        self.client.post(self.delete_url)
        self.assertFalse(Experience.objects.filter(pk=self.experience.pk).exists())

    def test_delete_requires_post(self):
        self.login_as(self.owner)
        self.client.get(self.delete_url)
        self.assertTrue(Experience.objects.filter(pk=self.experience.pk).exists())

    def test_controls_are_hidden_from_users_without_permission(self):
        expected = {
            None: (False, False, False),
            self.regular: (False, False, False),
            self.editor: (False, True, False),
            self.owner: (True, True, True),
        }
        for user, (add, edit, delete) in expected.items():
            self.client.logout()
            if user:
                self.login_as(user)
            html = self.client.get(reverse("main:show_experience")).content.decode()
            label = user.username if user else "visitor"
            self.assertEqual(self.create_url in html, add, f"Add button for {label}")
            self.assertEqual(self.update_url in html, edit, f"Edit button for {label}")
            self.assertEqual(self.delete_url in html, delete, f"Delete form for {label}")
            trigger = f'popovertarget="delete-experience-{self.experience.id}"'
            self.assertEqual(trigger in html, delete, f"Delete button for {label}")


class ExperienceStarTest(RoleTestCase):
    def test_toggle_adds_then_removes_the_star(self):
        self.login_as(self.regular)
        self.client.post(self.star_url)
        self.assertEqual(self.experience.starred_by.count(), 1)
        self.client.post(self.star_url)
        self.assertEqual(self.experience.starred_by.count(), 0)

    def test_one_star_per_user_and_every_role_can_star(self):
        for user in (self.regular, self.editor, self.owner):
            self.client.logout()
            self.login_as(user)
            self.client.post(self.star_url)
        self.assertEqual(self.experience.starred_by.count(), 3)

    def test_get_request_does_not_change_stars(self):
        self.login_as(self.regular)
        self.client.get(self.star_url)
        self.assertEqual(self.experience.starred_by.count(), 0)

    def test_page_shows_count_and_current_user_state(self):
        self.experience.starred_by.add(self.regular, self.editor)
        self.login_as(self.regular)
        html = self.client.get(reverse("main:show_experience")).content.decode()
        self.assertIn("Unstar", html)
        self.assertIn('<span class="star-count">2</span>', html)
        self.client.logout()
        self.assertNotIn("Unstar", self.client.get(reverse("main:show_experience")).content.decode())

    def test_star_on_missing_experience_returns_404(self):
        self.login_as(self.regular)
        missing = reverse("main:toggle_star_experience", args=["00000000-0000-0000-0000-000000000000"])
        self.assertEqual(self.client.post(missing).status_code, 404)


class ExperienceJsonApiTest(RoleTestCase):
    def test_json_is_public_and_lists_experiences(self):
        response = self.client.get(reverse("main:get_experience_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(json.loads(response.content)[0]["fields"]["title"], self.experience.title)

    def test_json_exposes_usernames_not_ids_or_sensitive_fields(self):
        self.experience.starred_by.add(self.regular)
        body = self.client.get(reverse("main:get_experience_json")).content.decode()
        starred_by = json.loads(body)[0]["fields"]["starred_by"]
        self.assertEqual(starred_by, [["regular"]])
        for leaked in ("password", "email", "is_superuser"):
            self.assertNotIn(leaked, body)


class ProjectPermissionTest(RoleTestCase):
    def test_only_owner_can_create_or_delete_project(self):
        project = Project.objects.create(title="VETO", role="Frontend", description="x", year="2026")
        delete_url = reverse("main:delete_project", args=[project.id])
        create_url = reverse("main:create_project")

        self.assertRedirects(self.client.get(create_url), f"/login/?next={create_url}", fetch_redirect_response=False)
        self.login_as(self.regular)
        self.assertEqual(self.client.get(create_url).status_code, 403)
        self.assertEqual(self.client.post(delete_url).status_code, 403)
        self.assertTrue(Project.objects.filter(pk=project.pk).exists())

        self.client.logout()
        self.login_as(self.owner)
        self.assertEqual(self.client.get(create_url).status_code, 200)
        self.client.post(delete_url)
        self.assertFalse(Project.objects.filter(pk=project.pk).exists())

    def test_project_star_toggle(self):
        project = Project.objects.create(title="VETO", role="Frontend", description="x", year="2026")
        url = reverse("main:toggle_star", args=[project.id])
        self.login_as(self.regular)
        self.client.post(url)
        self.assertEqual(project.starred_by.count(), 1)
        self.client.post(url)
        self.assertEqual(project.starred_by.count(), 0)


class AuthenticationTest(TestCase):
    def test_register_creates_user_and_redirects_to_login(self):
        response = self.client.post(reverse("main:register"), {
            "username": "newuser", "password1": PASSWORD, "password2": PASSWORD,
        })
        self.assertRedirects(response, reverse("main:login"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_register_rejects_mismatched_passwords(self):
        response = self.client.post(reverse("main:register"), {
            "username": "newuser", "password1": PASSWORD, "password2": "different",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="newuser").exists())

    def test_login_sets_last_login_cookie_and_logout_clears_it(self):
        User.objects.create_user("visitor", password=PASSWORD)
        response = self.client.post(reverse("main:login"), {"username": "visitor", "password": PASSWORD})
        self.assertRedirects(response, reverse("main:show_main"))
        self.assertIn("last_login", response.cookies)
        self.assertNotEqual(response.cookies["last_login"].value, "")

        response = self.client.get(reverse("main:logout"))
        self.assertEqual(response.cookies["last_login"]["max-age"], 0)

    def test_wrong_password_shows_error_without_logging_in(self):
        User.objects.create_user("visitor", password=PASSWORD)
        response = self.client.post(reverse("main:login"), {"username": "visitor", "password": "wrong"})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertNotIn("last_login", response.cookies)
