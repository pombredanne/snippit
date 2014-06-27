# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tags'
        db.create_table('tags', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, unique=True, populate_from='name', overwrite=False)),
        ))
        db.send_create_signal(u'snippet', ['Tags'])

        # Adding model 'Languages'
        db.create_table('languages', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, unique=True, populate_from='name', overwrite=False)),
        ))
        db.send_create_signal(u'snippet', ['Languages'])

        # Adding model 'Snippets'
        db.create_table('snippets', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.User'])),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, unique=True, populate_from='name', overwrite=False)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'snippet', ['Snippets'])

        # Adding M2M table for field tags on 'Snippets'
        m2m_table_name = db.shorten_name('snippets_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('snippets', models.ForeignKey(orm[u'snippet.snippets'], null=False)),
            ('tags', models.ForeignKey(orm[u'snippet.tags'], null=False))
        ))
        db.create_unique(m2m_table_name, ['snippets_id', 'tags_id'])

        # Adding model 'Pages'
        db.create_table('snippets_pages', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('snippet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['snippet.Snippets'])),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['snippet.Languages'])),
        ))
        db.send_create_signal(u'snippet', ['Pages'])

        # Adding model 'Comments'
        db.create_table('snippets_comments', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.User'])),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('snippet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['snippet.Snippets'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('create_ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
        ))
        db.send_create_signal(u'snippet', ['Comments'])

    def backwards(self, orm):
        # Deleting model 'Tags'
        db.delete_table('tags')

        # Deleting model 'Languages'
        db.delete_table('languages')

        # Deleting model 'Snippets'
        db.delete_table('snippets')

        # Removing M2M table for field tags on 'Snippets'
        db.delete_table(db.shorten_name('snippets_tags'))

        # Deleting model 'Pages'
        db.delete_table('snippets_pages')

        # Deleting model 'Comments'
        db.delete_table('snippets_comments')

    models = {
        u'account.user': {
            'Meta': {'object_name': 'User', 'db_table': "'users'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '65', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'recovery_key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'stars': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['snippet.Snippets']", 'symmetrical': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '65', 'null': 'True', 'blank': 'True'})
        },
        u'snippet.comments': {
            'Meta': {'object_name': 'Comments', 'db_table': "'snippets_comments'"},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.User']"}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'create_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'snippet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['snippet.Snippets']"})
        },
        u'snippet.languages': {
            'Meta': {'object_name': 'Languages', 'db_table': "'languages'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'unique': 'True', 'populate_from': "'name'", 'overwrite': 'False'})
        },
        u'snippet.pages': {
            'Meta': {'object_name': 'Pages', 'db_table': "'snippets_pages'"},
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['snippet.Languages']"}),
            'snippet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['snippet.Snippets']"})
        },
        u'snippet.snippets': {
            'Meta': {'object_name': 'Snippets', 'db_table': "'snippets'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'unique': 'True', 'populate_from': "'name'", 'overwrite': 'False'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['snippet.Tags']", 'symmetrical': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'snippet.tags': {
            'Meta': {'object_name': 'Tags', 'db_table': "'tags'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'unique': 'True', 'populate_from': "'name'", 'overwrite': 'False'})
        }
    }

    complete_apps = ['snippet']
