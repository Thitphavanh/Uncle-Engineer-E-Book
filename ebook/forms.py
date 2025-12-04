from django import forms
from .models import EBook, EBookImage, EBookCategory


class MultipleFileInput(forms.ClearableFileInput):
    """Custom widget สำหรับรองรับการอัพโหลดหลายไฟล์"""
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """Custom field สำหรับรองรับการอัพโหลดหลายไฟล์"""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class EBookForm(forms.ModelForm):
    """Form สำหรับสร้างและแก้ไข EBook"""

    # Field สำหรับอัพโหลดหลายรูปภาพ
    images = MultipleFileField(
        required=False,
        label='รูปภาพเพิ่มเติม (เลือกได้หลายรูป)',
        widget=MultipleFileInput(attrs={
            'accept': 'image/*',
            'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-black file:text-white hover:file:bg-gray-800 cursor-pointer'
        })
    )

    class Meta:
        model = EBook
        fields = ['category', 'title', 'descriptions', 'slug', 'price', 'is_available', 'cover_image']
        labels = {
            'category': 'หมวดหมู่',
            'title': 'ชื่อหนังสือ',
            'descriptions': 'รายละเอียด',
            'slug': 'Slug (URL Friendly)',
            'price': 'ราคา (บาท)',
            'is_available': 'เปิดให้บริการ',
            'cover_image': 'รูปปก (รูปหลัก)',
        }
        widgets = {
            'category': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-black focus:ring focus:ring-black focus:ring-opacity-50 px-4 py-2 border'
            }),
            'title': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-black focus:ring focus:ring-black focus:ring-opacity-50 px-4 py-2 border',
                'placeholder': 'กรอกชื่อหนังสือ'
            }),
            'descriptions': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-black focus:ring focus:ring-black focus:ring-opacity-50 px-4 py-2 border',
                'rows': 5,
                'placeholder': 'กรอกรายละเอียดหนังสือ'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-black focus:ring focus:ring-black focus:ring-opacity-50 px-4 py-2 border',
                'placeholder': 'กรอก slug สำหรับ URL'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-black focus:ring focus:ring-black focus:ring-opacity-50 px-4 py-2 border',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'rounded border-gray-300 text-black shadow-sm focus:border-black focus:ring focus:ring-black focus:ring-opacity-50'
            }),
            'cover_image': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-black file:text-white hover:file:bg-gray-800 cursor-pointer',
                'accept': 'image/*'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # เพิ่ม empty label สำหรับ category dropdown
        self.fields['category'].empty_label = "-- เลือกหมวดหมู่ --"
