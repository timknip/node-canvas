{
  'conditions': [
    ['OS=="win"', {
      'variables': {
        'GTK_Root%': 'C:/GTK',  # Set the location of GTK all-in-one bundle
        'with_jpeg%': 'false',
        'with_gif%': 'false',
        'with_rsvg%': 'false',
        'variables': { # Nest jpeg_root to evaluate it before with_jpeg
          'jpeg_root%': '<!(node ./util/win_jpeg_lookup)',
          'is_msys%': '<!(node ./util/win_msys_lookup)'
        },
        'jpeg_root%': '<(jpeg_root)', # Take value of nested variable
        'jpeg_dll%': 'jpeg62.dll',
        'jpeg_lib%': 'jpeg.lib',
        'is_msys%': '<(is_msys)',
        'conditions': [
          ['jpeg_root==""', {
            'with_jpeg%': 'false'
          }, {
            'with_jpeg%': 'true'
          }],
          ['is_msys=="true"', {
            'with_jpeg%': 'true',
            'with_gif%': 'true',
            'with_rsvg%': 'true',
            'GTK_Root%': 'C:/msys64/mingw64',
            'jpeg_root%': 'C:/msys64/mingw64',
            'jpeg_dll%': 'libjpeg-8.dll',
            'jpeg_lib%': 'libjpeg-8.lib'
          }, {
            'with_rsvg%': 'false'
          }]
        ]
      }
    }, {  # 'OS!="win"'
      'variables': {
        'with_jpeg%': '<!(node ./util/has_lib.js jpeg)',
        'with_gif%': '<!(node ./util/has_lib.js gif)',
        'with_rsvg%': '<!(node ./util/has_lib.js rsvg)'
      }
    }]
  ],
  'targets': [
    {
      'target_name': 'canvas-postbuild',
      'dependencies': ['canvas'],
      'conditions': [
        ['OS=="win" and is_msys==""', {
          'copies': [{
            'destination': '<(PRODUCT_DIR)',
            'files': [
              '<(GTK_Root)/bin/zlib1.dll',
              '<(GTK_Root)/bin/libintl-8.dll',
              '<(GTK_Root)/bin/libpng14-14.dll',
              '<(GTK_Root)/bin/libpangocairo-1.0-0.dll',
              '<(GTK_Root)/bin/libpango-1.0-0.dll',
              '<(GTK_Root)/bin/libpangoft2-1.0-0.dll',
              '<(GTK_Root)/bin/libpangowin32-1.0-0.dll',
              '<(GTK_Root)/bin/libcairo-2.dll',
              '<(GTK_Root)/bin/libfontconfig-1.dll',
              '<(GTK_Root)/bin/libfreetype-6.dll',
              '<(GTK_Root)/bin/libglib-2.0-0.dll',
              '<(GTK_Root)/bin/libgobject-2.0-0.dll',
              '<(GTK_Root)/bin/libgmodule-2.0-0.dll',
              '<(GTK_Root)/bin/libgthread-2.0-0.dll',
              '<(GTK_Root)/bin/libexpat-1.dll'
            ]
          }]
        }]
      ]
    },
    {
      'target_name': 'canvas',
      'include_dirs': ["<!(node -e \"require('nan')\")"],
      'sources': [
        'src/backend/Backend.cc',
        'src/backend/ImageBackend.cc',
        'src/backend/PdfBackend.cc',
        'src/backend/SvgBackend.cc',
        'src/Backends.cc',
        'src/Canvas.cc',
        'src/CanvasGradient.cc',
        'src/CanvasPattern.cc',
        'src/CanvasRenderingContext2d.cc',
        'src/closure.cc',
        'src/color.cc',
        'src/Image.cc',
        'src/ImageData.cc',
        'src/init.cc',
        'src/register_font.cc',
        'src/toBuffer.cc'
      ],
      'conditions': [
        ['is_msys=="true"', {
         'defines': [
            'HAVE_GIF',
            'HAVE_BOOLEAN', # or jmorecfg.h tries to define it
            '_USE_MATH_DEFINES' # for M_PI
          ],
          'libraries': [
            'C:/msys64/mingw64/lib/libcairo-2.lib',
            'C:/msys64/mingw64/lib/libpng16-16.lib',
            'C:/msys64/mingw64/lib/libjpeg-8.lib',
            'C:/msys64/mingw64/lib/libpango-1.0-0.lib',
            'C:/msys64/mingw64/lib/libpangocairo-1.0-0.lib',
            'C:/msys64/mingw64/lib/libgobject-2.0-0.lib',
            'C:/msys64/mingw64/lib/libglib-2.0-0.lib',
            'C:/msys64/mingw64/lib/libturbojpeg-0.lib',
            'C:/msys64/mingw64/lib/libgif-7.lib',
            'C:/msys64/mingw64/lib/libfreetype-6.lib',
            'C:/msys64/mingw64/lib/libpixman-1-0.lib'
          ],
          'include_dirs': [
            'C:/msys64/mingw64/include',
            'C:/msys64/mingw64/include/pango-1.0',
            'C:/msys64/mingw64/include/cairo',
            'C:/msys64/mingw64/include/libpng16',
            'C:/msys64/mingw64/include/glib-2.0',
            'C:/msys64/mingw64/lib/glib-2.0/include',
            'C:/msys64/mingw64/include/pixman-1',
            'C:/msys64/mingw64/include/freetype2',
            'C:/msys64/mingw64/include/fontconfig',
            'C:/msys64/mingw64/include/gdk-pixbuf-2.0',
          ],
          'configurations': {
            'Debug': {
              'msvs_settings': {
                'VCCLCompilerTool': {
                  'WarningLevel': 4,
                  'ExceptionHandling': 1,
                  'DisableSpecificWarnings': [
                    4100, 4127, 4201, 4244, 4267, 4506, 4611, 4714, 4512
                  ]
                }
              }
            },
            'Release': {
              'msvs_settings': {
                'VCCLCompilerTool': {
                  'WarningLevel': 4,
                  'ExceptionHandling': 1,
                  'DisableSpecificWarnings': [
                    4100, 4127, 4201, 4244, 4267, 4506, 4611, 4714, 4512
                  ]
                }
              }
            }
          }
        }],
        ['OS=="win" and is_msys==""', {
          'libraries': [
            '-l<(GTK_Root)/lib/cairo.lib',
            '-l<(GTK_Root)/lib/libpng.lib',
            '-l<(GTK_Root)/lib/pangocairo-1.0.lib',
            '-l<(GTK_Root)/lib/pango-1.0.lib',
            '-l<(GTK_Root)/lib/freetype.lib',
            '-l<(GTK_Root)/lib/glib-2.0.lib',
            '-l<(GTK_Root)/lib/gobject-2.0.lib'
          ],
          'include_dirs': [
            '<(GTK_Root)/include',
            '<(GTK_Root)/include/cairo',
            '<(GTK_Root)/include/pango-1.0',
            '<(GTK_Root)/include/glib-2.0',
            '<(GTK_Root)/include/freetype2',
            '<(GTK_Root)/lib/glib-2.0/include'
          ],
          'defines': [
            '_USE_MATH_DEFINES'  # for M_PI
          ],
          'configurations': {
            'Debug': {
              'msvs_settings': {
                'VCCLCompilerTool': {
                  'WarningLevel': 4,
                  'ExceptionHandling': 1,
                  'DisableSpecificWarnings': [
                    4100, 4127, 4201, 4244, 4267, 4506, 4611, 4714, 4512
                  ]
                }
              }
            },
            'Release': {
              'msvs_settings': {
                'VCCLCompilerTool': {
                  'WarningLevel': 4,
                  'ExceptionHandling': 1,
                  'DisableSpecificWarnings': [
                    4100, 4127, 4201, 4244, 4267, 4506, 4611, 4714, 4512
                  ]
                }
              }
            }
          }
        }],
        [ 'OS!="win"', {  # 'OS!="win"'
          'libraries': [
            '<!@(pkg-config pixman-1 --libs)',
            '<!@(pkg-config cairo --libs)',
            '<!@(pkg-config libpng --libs)',
            '<!@(pkg-config pangocairo --libs)',
            '<!@(pkg-config freetype2 --libs)'
          ],
          'include_dirs': [
            '<!@(pkg-config cairo --cflags-only-I | sed s/-I//g)',
            '<!@(pkg-config libpng --cflags-only-I | sed s/-I//g)',
            '<!@(pkg-config pangocairo --cflags-only-I | sed s/-I//g)',
            '<!@(pkg-config freetype2 --cflags-only-I | sed s/-I//g)'
          ]
        }],
        ['with_jpeg=="true"', {
          'defines': [
            'HAVE_JPEG'
          ],
          'conditions': [
            ['OS=="win"', {
              'include_dirs': [
                '<(jpeg_root)/include'
              ],
              'libraries': [
                '-l<(jpeg_root)/lib/<(jpeg_lib)',
              ]
            }, {
              'libraries': [
                '-ljpeg'
              ]
            }]
          ]
        }],
        ['with_gif=="true"', {
          'defines': [
            'HAVE_GIF'
          ],
          'conditions': [
            ['is_msys=="true"', {
              'libraries': [
                '-l<(GTK_Root)/lib/libgif-7.lib'
              ]
            }],
            ['OS=="win" and is_msys==""', {
              'libraries': [
                '-l<(GTK_Root)/lib/gif.lib'
              ]
            }],
            ['OS!="win"',{
              'libraries': [
                '-lgif'
              ]
            }]
          ]
        }],
        ['with_rsvg=="true"', {
          'defines': [
            'HAVE_RSVG'
          ],
          'conditions': [
            ['OS=="win"', {
              'libraries': [
                '-l<(GTK_Root)/lib/librsvg-2-2.lib'
              ],
              'include_dirs': [
                '<(GTK_Root)/include/librsvg-2.0'
              ]
            }, {
              'include_dirs': [
                '<!@(pkg-config librsvg-2.0 --cflags-only-I | sed s/-I//g)'
              ],
              'libraries': [
                '<!@(pkg-config librsvg-2.0 --libs)'
              ]
            }]
          ]
        }]
      ]
    }
  ]
}
