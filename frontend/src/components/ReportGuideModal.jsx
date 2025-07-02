import React from 'react'
import { Modal, Box, Typography, IconButton } from '@mui/material'
import CloseIcon from '@mui/icons-material/Close'

function ReportGuideModal({ open, onClose }) {
  return (
    <Modal open={open} onClose={onClose} aria-labelledby="report-guide-title">
      <Box
        sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          bgcolor: 'background.paper',
          boxShadow: 24,
          p: 3,
          borderRadius: 2,
          maxWidth: 600,
          width: '90%',
          maxHeight: '80%',
          overflowY: 'auto',
        }}
      >
        <IconButton
          aria-label="close"
          onClick={onClose}
          sx={{ position: 'absolute', top: 8, right: 8 }}
        >
          <CloseIcon />
        </IconButton>
        <Typography id="report-guide-title" variant="h6" sx={{ mb: 2 }}>
          Rapor Kılavuzu – Kaliteli ve Anlamlı Çıktı İçin İpuçları
        </Typography>
        <Typography variant="subtitle1" sx={{ fontWeight: 'bold', mt: 1 }}>
          a) Kısa Şikayetler, Yüzeysel Rapor:
        </Typography>
        <Typography variant="body2" paragraph>
          Eğer çok kısa şekilde şikayet yazarsanız (örneğin “kaynak kopması”, “parçada çapak”)
          oluşan rapor çok genel ve yüzeysel olacaktır. Yapay zeka asistanına parça ve problem
          ile ilgili ne kadar detay verirseniz, o kadar iyi ve size özel bir çıktı alabilirsiniz.
        </Typography>
        <Typography variant="subtitle1" sx={{ fontWeight: 'bold', mt: 2 }}>
          b) Departman ve Ünvanları Özelleştirin:
        </Typography>
        <Typography variant="body2" paragraph>
          Yapay zeka raporu oluştururken işletmenizin yapısını ve departman isimlerini net olarak
          bilemez. Raporda olmasını ya da olmamasını istediğiniz departman isimlerini ya da
          ünvanları “Özel Şartlar” kısmına ekleyerek yönetebilirsiniz.
        </Typography>
        <Typography variant="subtitle1" sx={{ fontWeight: 'bold', mt: 2 }}>
          c) Özel Şartlar Her Zaman Göz Önünde:
        </Typography>
        <Typography variant="body2" paragraph>
          Özel Şartlar bölümüne yazacağınız her kelime, doğrudan yapay zekâya talimat olarak
          gönderilir ve rapor oluşturulurken dikkate alınır.
        </Typography>
        <Typography variant="subtitle1" sx={{ fontWeight: 'bold', mt: 2 }}>
          Ekstra İpuçları:
        </Typography>
        <Typography variant="body2" component="div">
          <ul>
            <li>Somut Olaylar Yazın: Şikayetinizi örnekle açıklayın. (Ör: “25 Mayıs’ta 5 adet ürünün bağlantı noktasında çatlak tespit edildi, numuneler ekte.”)</li>
            <li>Beklediğiniz Sonuçları Netleştirin: Raporda yer almasını istediğiniz özel iyileştirme adımlarını veya önlemleri belirtin.</li>
            <li>Teknik Terim ve Kısaltmalara Dikkat: Varsa açıklamalarını ekleyin, yanlış yönlendirmeleri önleyin.</li>
            <li>İstenmeyen Bölümleri Belirtin: Raporda istemediğiniz, gereksiz bulduğunuz başlıkları “Özel Şartlar”a ekleyerek hariç tutabilirsiniz.</li>
          </ul>
        </Typography>
      </Box>
    </Modal>
  )
}

export default ReportGuideModal
