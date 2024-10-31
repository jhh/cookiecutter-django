from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.urls import reverse_lazy


class ExampleForm(forms.Form):
    like_website = forms.TypedChoiceField(
        label="Do you like this website?",
        choices=((1, "Yes"), (0, "No")),
        coerce=lambda x: bool(int(x)),
        widget=forms.RadioSelect,
        initial="1",
        required=True,
    )

    favorite_color = forms.ChoiceField(
        label="What is your favorite color?",
        choices=(("red", "Red"), ("blue", "Blue"), ("green", "Green")),
        required=False,
    )

    favorite_number = forms.IntegerField(
        label="Favorite number",
        help_text="Enter the favorite number",
        required=True,
    )

    notes = forms.CharField(
        label="Additional notes or feedback",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "index-form"
        # self.helper.form_method = "post"
        # self.helper.form_action = "home_page"
        self.helper.attrs = {
            "hx-post": reverse_lazy("home_page"),
            "hx-target": "#index-form",
            "hx-swap": "outerHTML",
        }

        self.helper.add_input(Submit("submit", "Submit"))